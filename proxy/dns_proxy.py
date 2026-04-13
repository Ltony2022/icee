#!/usr/bin/env python3
"""Simple DNS UDP proxy with domain-level blocking and traffic logging."""

from __future__ import annotations

import argparse
import atexit
import json
import logging
import os
import signal
import socket
import struct
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


QTYPE_NAMES = {
    1: "A",
    2: "NS",
    5: "CNAME",
    6: "SOA",
    12: "PTR",
    15: "MX",
    16: "TXT",
    28: "AAAA",
    33: "SRV",
    255: "ANY",
}

RCODE_NAMES = {
    0: "NOERROR",
    1: "FORMERR",
    2: "SERVFAIL",
    3: "NXDOMAIN",
    4: "NOTIMP",
    5: "REFUSED",
}


@dataclass(frozen=True)
class DNSQuestion:
    qname: str
    qtype: int
    qclass: int


def normalize_domain(domain: str) -> str:
    return domain.strip().rstrip(".").lower()


def type_name(qtype: int) -> str:
    return QTYPE_NAMES.get(qtype, f"TYPE{qtype}")


def rcode_name(rcode: int) -> str:
    return RCODE_NAMES.get(rcode, f"RCODE{rcode}")


def decode_name(packet: bytes, offset: int) -> tuple[str, int]:
    labels: list[str] = []
    jumped = False
    next_offset = offset
    visited_offsets: set[int] = set()

    while True:
        if offset >= len(packet):
            raise ValueError("DNS name offset out of range")

        length = packet[offset]

        if length == 0:
            offset += 1
            if not jumped:
                next_offset = offset
            break

        if (length & 0xC0) == 0xC0:
            if offset + 1 >= len(packet):
                raise ValueError("Truncated DNS compression pointer")
            pointer = ((length & 0x3F) << 8) | packet[offset + 1]
            if pointer in visited_offsets:
                raise ValueError("Compression pointer loop")
            visited_offsets.add(pointer)
            if not jumped:
                next_offset = offset + 2
                jumped = True
            offset = pointer
            continue

        if (length & 0xC0) != 0:
            raise ValueError("Unsupported DNS label format")

        offset += 1
        end = offset + length
        if end > len(packet):
            raise ValueError("Truncated DNS label")
        labels.append(packet[offset:end].decode("ascii", errors="replace"))
        offset = end
        if not jumped:
            next_offset = offset

    return ".".join(labels), next_offset


def skip_questions(packet: bytes, qdcount: int, offset: int = 12) -> int:
    for _ in range(qdcount):
        _, offset = decode_name(packet, offset)
        if offset + 4 > len(packet):
            raise ValueError("Truncated DNS question")
        offset += 4
    return offset


def parse_first_question(packet: bytes) -> DNSQuestion | None:
    if len(packet) < 12:
        raise ValueError("Packet too short for DNS header")
    _, _, qdcount, _, _, _ = struct.unpack("!HHHHHH", packet[:12])
    if qdcount == 0:
        return None

    offset = 12
    qname, offset = decode_name(packet, offset)
    if offset + 4 > len(packet):
        raise ValueError("Truncated DNS question")
    qtype, qclass = struct.unpack("!HH", packet[offset : offset + 4])
    return DNSQuestion(normalize_domain(qname), qtype, qclass)


def format_rdata(packet: bytes, rtype: int, rdata_offset: int, rdlength: int) -> str:
    rdata = packet[rdata_offset : rdata_offset + rdlength]

    if rtype == 1 and rdlength == 4:
        return socket.inet_ntoa(rdata)

    if rtype == 28 and rdlength == 16:
        return socket.inet_ntop(socket.AF_INET6, rdata)

    if rtype in {2, 5, 12}:
        name, _ = decode_name(packet, rdata_offset)
        return normalize_domain(name)

    if rtype == 15 and rdlength >= 3:
        preference = struct.unpack("!H", packet[rdata_offset : rdata_offset + 2])[0]
        exchange, _ = decode_name(packet, rdata_offset + 2)
        return f"{preference} {normalize_domain(exchange)}"

    return rdata.hex()


def parse_response_summary(packet: bytes) -> tuple[int, list[str]]:
    if len(packet) < 12:
        return 0, []

    _, flags, qdcount, ancount, _, _ = struct.unpack("!HHHHHH", packet[:12])
    rcode = flags & 0x000F
    answers: list[str] = []

    try:
        offset = skip_questions(packet, qdcount)
        for _ in range(ancount):
            name, offset = decode_name(packet, offset)
            if offset + 10 > len(packet):
                break
            rtype, _rclass, _ttl, rdlength = struct.unpack(
                "!HHIH", packet[offset : offset + 10]
            )
            offset += 10
            if offset + rdlength > len(packet):
                break
            rdata_text = format_rdata(packet, rtype, offset, rdlength)
            offset += rdlength
            answers.append(f"{normalize_domain(name)} {type_name(rtype)} {rdata_text}")
            if len(answers) >= 5:
                break
    except ValueError:
        return rcode, []

    return rcode, answers


def build_response_with_rcode(query_packet: bytes, rcode: int) -> bytes:
    if len(query_packet) < 12:
        return b""

    txid, flags, qdcount, _, _, _ = struct.unpack("!HHHHHH", query_packet[:12])
    try:
        q_end = skip_questions(query_packet, qdcount)
        question_section = query_packet[12:q_end]
    except ValueError:
        qdcount = 0
        question_section = b""

    response_flags = (
        0x8000  # QR = response
        | (flags & 0x7800)  # keep OPCODE
        | (flags & 0x0110)  # keep RD + CD
        | 0x0080  # RA = recursion available
        | (rcode & 0x000F)
    )
    header = struct.pack("!HHHHHH", txid, response_flags, qdcount, 0, 0, 0)
    return header + question_section


def is_blocked_domain(domain: str, blocked_domains: set[str]) -> bool:
    normalized = normalize_domain(domain)
    for blocked in blocked_domains:
        if normalized == blocked or normalized.endswith(f".{blocked}"):
            return True
    return False


def load_blocked_domains(cli_domains: list[str], block_file: Path | None) -> set[str]:
    blocked = {
        normalize_domain(domain) for domain in cli_domains if normalize_domain(domain)
    }

    if block_file is not None:
        with block_file.open("r", encoding="utf-8") as handle:
            for line in handle:
                item = line.strip()
                if not item or item.startswith("#"):
                    continue
                blocked_item = normalize_domain(item)
                if blocked_item:
                    blocked.add(blocked_item)

    return blocked


def forward_to_upstream(
    packet: bytes, upstream: tuple[str, int], timeout: float
) -> bytes:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as upstream_sock:
        upstream_sock.settimeout(timeout)
        upstream_sock.sendto(packet, upstream)
        response, _ = upstream_sock.recvfrom(65535)
        return response


def handle_packet(
    packet: bytes,
    client_addr: tuple[str, int],
    server_sock: socket.socket,
    upstream: tuple[str, int],
    timeout: float,
    blocked_domains: set[str],
) -> None:
    client_host, client_port = client_addr
    question: DNSQuestion | None = None

    try:
        question = parse_first_question(packet)
    except ValueError as exc:
        logging.warning("IN  %s:%d malformed query (%s)", client_host, client_port, exc)

    domain = question.qname if question else "<unknown>"
    qtype = type_name(question.qtype) if question else "UNKNOWN"
    logging.info("IN  %s:%d -> %s (%s)", client_host, client_port, domain, qtype)

    if question and is_blocked_domain(question.qname, blocked_domains):
        blocked_response = build_response_with_rcode(packet, rcode=3)
        server_sock.sendto(blocked_response, client_addr)
        logging.info(
            "OUT %s:%d <- %s (%s) BLOCKED NXDOMAIN",
            client_host,
            client_port,
            domain,
            qtype,
        )
        return

    try:
        response = forward_to_upstream(packet, upstream, timeout)
    except socket.timeout:
        servfail = build_response_with_rcode(packet, rcode=2)
        server_sock.sendto(servfail, client_addr)
        logging.warning(
            "OUT %s:%d <- %s (%s) upstream timeout, returned SERVFAIL",
            client_host,
            client_port,
            domain,
            qtype,
        )
        return
    except OSError as exc:
        servfail = build_response_with_rcode(packet, rcode=2)
        server_sock.sendto(servfail, client_addr)
        logging.error(
            "OUT %s:%d <- %s (%s) upstream error (%s), returned SERVFAIL",
            client_host,
            client_port,
            domain,
            qtype,
            exc,
        )
        return

    server_sock.sendto(response, client_addr)
    rcode, answers = parse_response_summary(response)
    if answers:
        answer_str = "; ".join(answers)
        logging.info(
            "OUT %s:%d <- %s (%s) %s answers=%s",
            client_host,
            client_port,
            domain,
            qtype,
            rcode_name(rcode),
            answer_str,
        )
    else:
        logging.info(
            "OUT %s:%d <- %s (%s) %s answers=none",
            client_host,
            client_port,
            domain,
            qtype,
            rcode_name(rcode),
        )


DNS_BACKUP_FILE = Path(__file__).parent / "dns_backup.json"


def _run_powershell(script: str) -> str:
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def get_active_interface() -> str | None:
    """Return the alias of the first interface that has a default gateway."""
    script = (
        "Get-NetRoute -DestinationPrefix '0.0.0.0/0' "
        "| Sort-Object RouteMetric "
        "| Select-Object -First 1 -ExpandProperty InterfaceIndex "
        "| ForEach-Object { (Get-NetAdapter -InterfaceIndex $_).Name }"
    )
    name = _run_powershell(script)
    return name if name else None


def get_current_dns(interface: str) -> list[str]:
    """Return the DNS server addresses configured on *interface*."""
    script = (
        f"(Get-DnsClientServerAddress -InterfaceAlias '{interface}' "
        "-AddressFamily IPv4).ServerAddresses"
    )
    output = _run_powershell(script)
    return [line.strip() for line in output.splitlines() if line.strip()]


def set_dns(interface: str, servers: list[str]) -> None:
    """Set DNS servers on *interface*. An empty list resets to DHCP."""
    if servers:
        addr_list = ",".join(f"'{s}'" for s in servers)
        script = (
            f"Set-DnsClientServerAddress -InterfaceAlias '{interface}' "
            f"-ServerAddresses ({addr_list})"
        )
    else:
        script = f"Set-DnsClientServerAddress -InterfaceAlias '{interface}' -ResetServerAddresses"
    _run_powershell(script)


def save_dns_backup(interface: str, servers: list[str]) -> None:
    """Persist the original DNS settings to disk so they survive hard crashes."""
    data = {"interface": interface, "servers": servers}
    DNS_BACKUP_FILE.write_text(json.dumps(data), encoding="utf-8")
    logging.info("Saved original DNS backup to %s", DNS_BACKUP_FILE)


def load_dns_backup() -> tuple[str, list[str]] | None:
    """Load a previously saved DNS backup, if it exists."""
    if not DNS_BACKUP_FILE.exists():
        return None
    try:
        data = json.loads(DNS_BACKUP_FILE.read_text(encoding="utf-8"))
        return data["interface"], data["servers"]
    except (json.JSONDecodeError, KeyError):
        return None


def remove_dns_backup() -> None:
    DNS_BACKUP_FILE.unlink(missing_ok=True)


def write_pid_file(pid_file: Path | None) -> bool:
    if pid_file is None:
        return False
    pid_file.write_text(str(os.getpid()), encoding="utf-8")
    return True


def remove_pid_file(pid_file: Path | None, expected_pid: int | None = None) -> None:
    if pid_file is None:
        return
    if not pid_file.exists():
        return
    if expected_pid is not None:
        try:
            pid_in_file = int(pid_file.read_text(encoding="utf-8").strip())
        except (OSError, ValueError):
            return
        if pid_in_file != expected_pid:
            return
    pid_file.unlink(missing_ok=True)


def stop_requested(stop_file: Path | None) -> bool:
    return bool(stop_file is not None and stop_file.exists())


def remove_stop_file(stop_file: Path | None) -> None:
    if stop_file is None:
        return
    stop_file.unlink(missing_ok=True)


def restore_dns() -> None:
    """Restore the original DNS from the backup file."""
    backup = load_dns_backup()
    if backup is None:
        return
    interface, servers = backup
    logging.info("Restoring DNS on '%s' to %s", interface, servers or "DHCP")
    try:
        set_dns(interface, servers)
        logging.info("DNS restored successfully.")
    except Exception as exc:
        logging.error("Failed to restore DNS: %s", exc)
    finally:
        remove_dns_backup()


def save_blocked_domains_to_file(
    blocked_domains: set[str], block_file: Path | None
) -> None:
    """Write the current blocked domains list to disk."""
    target = block_file or Path(__file__).parent / "blocked_domains.txt"
    lines = ["# One domain per line.", "# Subdomains are also blocked.", ""]
    lines.extend(sorted(blocked_domains))
    lines.append("")
    target.write_text("\n".join(lines), encoding="utf-8")
    logging.info("Saved %d blocked domain(s) to %s", len(blocked_domains), target)


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="DNS UDP proxy that logs traffic and blocks selected domains."
    )
    parser.add_argument(
        "--listen-host", default="127.0.0.1", help="Local host to bind to."
    )
    parser.add_argument(
        "--listen-port", type=int, default=5353, help="Local UDP port to bind to."
    )
    parser.add_argument(
        "--upstream-host", default="1.1.1.1", help="Upstream DNS server host."
    )
    parser.add_argument(
        "--upstream-port", type=int, default=53, help="Upstream DNS server port."
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=2.0,
        help="Upstream query timeout in seconds.",
    )
    parser.add_argument(
        "--block",
        action="append",
        default=[],
        metavar="DOMAIN",
        help="Domain to block. Can be repeated. Subdomains are also blocked.",
    )
    parser.add_argument(
        "--block-file",
        type=Path,
        default=None,
        help="Text file with one blocked domain per line (# for comments).",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level.",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=None,
        help="Optional file path to write logs to (in addition to console).",
    )
    parser.add_argument(
        "--pid-file",
        type=Path,
        default=None,
        help="Optional file path used to publish the running proxy PID.",
    )
    parser.add_argument(
        "--stop-file",
        type=Path,
        default=None,
        help="Optional file path used by controller to request graceful shutdown.",
    )
    return parser


def main() -> None:
    args = make_parser().parse_args()

    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if args.log_file is not None:
        handlers.append(logging.FileHandler(args.log_file, encoding="utf-8"))

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=handlers,
        force=True,  # Override existing logging setup from IDE/debugger sessions.
    )

    blocked_domains = load_blocked_domains(args.block, args.block_file)
    block_file_mtime: float = 0.0
    if args.block_file and args.block_file.exists():
        block_file_mtime = args.block_file.stat().st_mtime
    upstream = (args.upstream_host, args.upstream_port)

    # --- DNS hijack setup ---
    interface = get_active_interface()
    if interface is None:
        logging.error("Could not detect an active network interface. Exiting.")
        sys.exit(1)

    original_dns = get_current_dns(interface)
    logging.info(
        "Active interface: '%s', current DNS: %s", interface, original_dns or "DHCP"
    )

    # --- Cleanup: restore DNS + save config on any exit ---
    cleanup_done = False
    dns_hijacked = False
    pid_file_written = False
    saw_stop_request = False

    def cleanup() -> None:
        nonlocal cleanup_done, dns_hijacked, pid_file_written, saw_stop_request
        if cleanup_done:
            return
        cleanup_done = True
        logging.info("Shutting down — running cleanup...")
        save_blocked_domains_to_file(blocked_domains, args.block_file)
        if dns_hijacked:
            restore_dns()
        if pid_file_written:
            remove_pid_file(args.pid_file, expected_pid=os.getpid())
        if saw_stop_request:
            remove_stop_file(args.stop_file)

    atexit.register(cleanup)

    def signal_handler(signum: int, _frame: object) -> None:
        sig_name = signal.Signals(signum).name
        logging.info("Received %s, cleaning up...", sig_name)
        cleanup()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # --- Main loop ---
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_sock:
        try:
            server_sock.bind((args.listen_host, args.listen_port))
        except OSError as exc:
            logging.error(
                "Failed to bind DNS proxy on %s:%d (%s).",
                args.listen_host,
                args.listen_port,
                exc,
            )
            sys.exit(1)
        server_sock.settimeout(1.0)
        pid_file_written = write_pid_file(args.pid_file)

        # Persist backup to disk first so it survives hard crashes.
        save_dns_backup(interface, original_dns)

        # Point system DNS to our proxy only after bind succeeds.
        proxy_dns = [args.listen_host]
        logging.info("Setting DNS on '%s' to %s", interface, proxy_dns)
        set_dns(interface, proxy_dns)
        dns_hijacked = True
        logging.info(
            "DNS proxy listening on %s:%d -> upstream %s:%d",
            args.listen_host,
            args.listen_port,
            args.upstream_host,
            args.upstream_port,
        )
        if blocked_domains:
            logging.info(
                "Blocking %d domain(s): %s",
                len(blocked_domains),
                ", ".join(sorted(blocked_domains)),
            )
        else:
            logging.info("No blocked domains configured.")

        while True:
            if stop_requested(args.stop_file):
                saw_stop_request = True
                logging.info("Stop request received. Shutting down gracefully...")
                break

            # Hot-reload blocked domains when the file changes on disk.
            if args.block_file and args.block_file.exists():
                current_mtime = args.block_file.stat().st_mtime
                if current_mtime != block_file_mtime:
                    block_file_mtime = current_mtime
                    blocked_domains = load_blocked_domains(args.block, args.block_file)
                    logging.info(
                        "Reloaded block list: %d domain(s)", len(blocked_domains)
                    )

            try:
                packet, client_addr = server_sock.recvfrom(65535)
            except socket.timeout:
                continue
            except ConnectionResetError:
                # Windows raises this when a previous UDP send got an ICMP
                # "port unreachable" reply. Safe to ignore.
                continue
            handle_packet(
                packet,
                client_addr,
                server_sock,
                upstream,
                args.timeout,
                blocked_domains,
            )


if __name__ == "__main__":
    main()
