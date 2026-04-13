import json
import importlib
import os
import signal
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from src.core.exception.django_exception import method_not_allowed

IS_FROZEN = bool(getattr(sys, "frozen", False))


def _resolve_proxy_script_path() -> Path:
    if IS_FROZEN:
        candidates: list[Path] = [Path(sys.executable).resolve().parent / "proxy" / "dns_proxy.py"]
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            candidates.append(Path(meipass) / "proxy" / "dns_proxy.py")
        for path in candidates:
            if path.exists():
                return path
        return candidates[0]
    return Path(__file__).resolve().parent.parent.parent.parent.parent / "proxy" / "dns_proxy.py"


def _resolve_blocked_domains_file() -> Path | None:
    if IS_FROZEN:
        candidates: list[Path] = [
            Path(sys.executable).resolve().parent / "proxy" / "blocked_domains.txt"
        ]
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            candidates.append(Path(meipass) / "proxy" / "blocked_domains.txt")
        for path in candidates:
            if path.exists():
                return path
        return None

    candidate = Path(__file__).resolve().parent.parent.parent.parent.parent / "proxy" / "blocked_domains.txt"
    return candidate if candidate.exists() else None


PROXY_SCRIPT = _resolve_proxy_script_path()
PROXY_DIR = (
    Path(tempfile.gettempdir()) / "icee-utils" / "proxy"
    if IS_FROZEN
    else PROXY_SCRIPT.parent
)
PROXY_DIR.mkdir(parents=True, exist_ok=True)
BLOCKED_DOMAINS_FILE = _resolve_blocked_domains_file()
LOG_FILE = PROXY_DIR / "dns_proxy.log"
PID_FILE = PROXY_DIR / "dns_proxy.pid"
STOP_FILE = PROXY_DIR / "dns_proxy.stop"

# Module-level process handle for the DNS proxy subprocess.
_proxy_process: subprocess.Popen | None = None
_proxy_pid: int | None = None
_pyuac_module: object | None = None
_pyuac_checked = False


def _get_pyuac():
    global _pyuac_module, _pyuac_checked
    if not _pyuac_checked:
        _pyuac_checked = True
        try:
            _pyuac_module = importlib.import_module("pyuac")
        except ImportError:
            _pyuac_module = None
    return _pyuac_module


def _clear_pid_file() -> None:
    PID_FILE.unlink(missing_ok=True)


def _clear_stop_file() -> None:
    STOP_FILE.unlink(missing_ok=True)


def _request_graceful_stop() -> None:
    STOP_FILE.write_text(str(time.time()), encoding="utf-8")


def _read_pid_file() -> int | None:
    if not PID_FILE.exists():
        return None
    try:
        raw = PID_FILE.read_text(encoding="utf-8").strip()
        if not raw:
            return None
        return int(raw)
    except (OSError, ValueError):
        return None


def _is_pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except PermissionError:
        # A permission error here still means the process exists.
        return True
    except OSError:
        return False
    return True


def _resolve_running_pid() -> int | None:
    """Resolve the DNS proxy PID for local or elevated process modes."""
    global _proxy_process, _proxy_pid

    if _proxy_process is not None:
        if _proxy_process.poll() is None:
            _proxy_pid = _proxy_process.pid
            return _proxy_pid
        _proxy_process = None

    pid = _proxy_pid or _read_pid_file()
    if pid is None:
        return None
    if _is_pid_alive(pid):
        _proxy_pid = pid
        return pid

    _proxy_pid = None
    _clear_pid_file()
    return None


def _is_admin() -> bool:
    if os.name != "nt":
        return True
    pyuac_module = _get_pyuac()
    if pyuac_module is None:
        return False
    return bool(pyuac_module.isUserAdmin())


def _wait_for_pid_file(timeout_seconds: float = 30.0) -> int | None:
    """Wait briefly for the elevated proxy process to publish its PID."""
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        pid = _read_pid_file()
        if pid is not None and _is_pid_alive(pid):
            return pid
        time.sleep(0.1)
    return None


def _wait_for_pid_exit(pid: int, timeout_seconds: float = 15.0) -> bool:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if not _is_pid_alive(pid):
            return True
        tracked_pid = _read_pid_file()
        # Graceful cleanup in dns_proxy.py removes both files.
        if tracked_pid != pid and not STOP_FILE.exists():
            return True
        time.sleep(0.2)
    tracked_pid = _read_pid_file()
    return (not _is_pid_alive(pid)) or (tracked_pid != pid and not STOP_FILE.exists())


def _is_pid_still_active(pid: int) -> bool:
    tracked_pid = _read_pid_file()
    if tracked_pid != pid:
        return False
    return _is_pid_alive(pid)


def _is_proxy_running() -> bool:
    """Check if the DNS proxy subprocess is currently running."""
    return _resolve_running_pid() is not None


def _is_udp_port_available(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
        try:
            probe.bind((host, port))
        except OSError:
            return False
    return True


def get_proxy_status(request):
    """GET /api/dns-proxy/status/ - Check if the DNS proxy is running."""
    if request.method == "GET":
        pid = _resolve_running_pid()
        running = pid is not None
        data = {"running": running}
        if running:
            data["pid"] = pid
        return JsonResponse(data)
    else:
        return method_not_allowed(request)


@csrf_exempt
def start_proxy(request):
    """POST /api/dns-proxy/start/ - Start the DNS proxy subprocess.

    Optional body: {
        "listen_host": "127.0.0.1",
        "listen_port": 5353,
        "upstream_host": "1.1.1.1",
        "upstream_port": 53,
        "timeout": 2.0,
        "log_level": "INFO"
    }
    """
    global _proxy_process, _proxy_pid

    if request.method == "POST":
        running_pid = _resolve_running_pid()
        if running_pid is not None:
            return JsonResponse(
                {"error": "proxy is already running", "pid": running_pid},
                status=409,
            )

        # Parse optional configuration from request body.
        config = {}
        if request.body:
            try:
                config = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "invalid JSON payload"}, status=400)

        if not PROXY_SCRIPT.exists():
            return JsonResponse(
                {"error": f"dns proxy worker script not found: {PROXY_SCRIPT}"},
                status=500,
            )

        if IS_FROZEN:
            # In packaged mode sys.executable is backend-service.exe, not python.exe.
            cmd = [sys.executable, "--dns-proxy-worker"]
        else:
            cmd = [sys.executable, str(PROXY_SCRIPT)]

        listen_host = config.get("listen_host", "127.0.0.1")
        listen_port = config.get("listen_port", 53)
        upstream_host = config.get("upstream_host", "1.1.1.1")
        upstream_port = config.get("upstream_port", 53)
        timeout = config.get("timeout", 2.0)
        log_level = config.get("log_level", "INFO")

        cmd.extend(["--listen-host", str(listen_host)])
        cmd.extend(["--listen-port", str(listen_port)])
        cmd.extend(["--upstream-host", str(upstream_host)])
        cmd.extend(["--upstream-port", str(upstream_port)])
        cmd.extend(["--timeout", str(timeout)])
        cmd.extend(["--log-level", str(log_level)])

        if BLOCKED_DOMAINS_FILE is not None and BLOCKED_DOMAINS_FILE.exists():
            cmd.extend(["--block-file", str(BLOCKED_DOMAINS_FILE)])

        cmd.extend(["--log-file", str(LOG_FILE)])
        cmd.extend(["--pid-file", str(PID_FILE)])
        cmd.extend(["--stop-file", str(STOP_FILE)])

        if not _is_udp_port_available(listen_host, int(listen_port)):
            # Either a stale/protected process is already bound or another app owns it.
            running_pid = _resolve_running_pid()
            payload = {
                "error": f"listen address {listen_host}:{listen_port} is already in use"
            }
            if running_pid is not None:
                payload["pid"] = running_pid
            return JsonResponse(payload, status=409)

        _clear_stop_file()

        if os.name == "nt" and not _is_admin():
            pyuac_module = _get_pyuac()
            if pyuac_module is None:
                return JsonResponse(
                    {
                        "error": "pyuac is required to start DNS proxy with administrator privileges."
                    },
                    status=500,
                )
            try:
                # Spawn the proxy as Administrator via UAC.
                pyuac_module.runAsAdmin(cmdLine=cmd, wait=False)
            except Exception as exc:
                return JsonResponse(
                    {"error": f"failed to elevate proxy start: {exc}"},
                    status=500,
                )

            elevated_pid = _wait_for_pid_file()
            if elevated_pid is None:
                return JsonResponse(
                    {
                        "error": "administrator permission was not granted in time. Please accept the UAC prompt and try again."
                    },
                    status=403,
                )

            _proxy_process = None
            _proxy_pid = elevated_pid
        else:
            creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            _proxy_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=creationflags,
            )
            _proxy_pid = _proxy_process.pid

        return JsonResponse(
            {
                "status": "started",
                "pid": _proxy_pid,
                "config": {
                    "listen_host": listen_host,
                    "listen_port": listen_port,
                    "upstream_host": upstream_host,
                    "upstream_port": upstream_port,
                    "timeout": timeout,
                    "log_level": log_level,
                },
            }
        )
    else:
        return method_not_allowed(request)


@csrf_exempt
def stop_proxy(request):
    """POST /api/dns-proxy/stop/ - Stop the DNS proxy subprocess."""
    global _proxy_process, _proxy_pid

    if request.method == "POST":
        if not _is_proxy_running():
            return JsonResponse({"error": "proxy is not running"}, status=409)

        pid = _resolve_running_pid()
        if pid is None:
            return JsonResponse({"error": "proxy is not running"}, status=409)

        # Ask the proxy process to exit itself so it can restore DNS and save state.
        try:
            _request_graceful_stop()
        except OSError as exc:
            return JsonResponse(
                {"error": f"failed to request graceful stop: {exc}"},
                status=500,
            )
        stopped_gracefully = _wait_for_pid_exit(pid, timeout_seconds=15.0)

        if not stopped_gracefully and not _is_pid_still_active(pid):
            stopped_gracefully = True

        if stopped_gracefully:
            if _proxy_process is not None:
                try:
                    _proxy_process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    pass
        elif _proxy_process is not None:
            _proxy_process.terminate()
            try:
                _proxy_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                _proxy_process.kill()
                _proxy_process.wait(timeout=5)
        elif os.name == "nt":
            taskkill_cmd = ["taskkill", "/PID", str(pid), "/T", "/F"]
            try:
                if _is_admin():
                    result = subprocess.run(
                        taskkill_cmd, capture_output=True, text=True, check=False
                    )
                    if result.returncode != 0:
                        if not _is_pid_still_active(pid):
                            result = None
                        else:
                            return JsonResponse(
                                {"error": result.stderr.strip() or result.stdout.strip()},
                                status=500,
                            )
                else:
                    pyuac_module = _get_pyuac()
                    if pyuac_module is None:
                        return JsonResponse(
                            {"error": "pyuac is required to stop elevated DNS proxy."},
                            status=500,
                        )
                    rc = pyuac_module.runAsAdmin(cmdLine=taskkill_cmd, wait=True)
                    if rc not in (0, None):
                        if not _is_pid_still_active(pid):
                            rc = 0
                        else:
                            return JsonResponse(
                                {
                                    "error": f"failed to stop elevated proxy (taskkill rc={rc})"
                                },
                                status=500,
                            )
            except Exception as exc:
                return JsonResponse(
                    {"error": f"failed to stop elevated DNS proxy: {exc}"},
                    status=500,
                )
        else:
            os.kill(pid, signal.SIGTERM)

        _proxy_process = None
        _proxy_pid = None
        _clear_pid_file()
        _clear_stop_file()
        return JsonResponse({"status": "stopped", "pid": pid, "graceful": stopped_gracefully})
    else:
        return method_not_allowed(request)
