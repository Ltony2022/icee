import json
import subprocess
import sys
from pathlib import Path

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from dns_proxy.api.proxy_control import BLOCKED_DOMAINS_FILE as _RESOLVED_FILE
from dns_proxy.api.proxy_control import PROXY_DIR
from src.core.exception.django_exception import method_not_allowed


BLOCKED_DOMAINS_FILE = _RESOLVED_FILE or (PROXY_DIR / "blocked_domains.txt")


def _load_blocked_domains() -> list[str]:
    """Read the blocked domains file and return a sorted list of domains."""
    if not BLOCKED_DOMAINS_FILE.exists():
        return []
    domains = []
    for line in BLOCKED_DOMAINS_FILE.read_text(encoding="utf-8").splitlines():
        item = line.strip()
        if not item or item.startswith("#"):
            continue
        domains.append(item.lower())
    return sorted(set(domains))


def _save_blocked_domains(domains: list[str]) -> None:
    """Write the blocked domains list back to file."""
    BLOCKED_DOMAINS_FILE.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# One domain per line.", "# Subdomains are also blocked.", ""]
    lines.extend(sorted(set(d.strip().lower() for d in domains if d.strip())))
    lines.append("")
    BLOCKED_DOMAINS_FILE.write_text("\n".join(lines), encoding="utf-8")


def _flush_dns_cache() -> None:
    """Flush the OS DNS cache so blocked/unblocked domains take effect immediately."""
    if sys.platform == "win32":
        subprocess.run(
            ["ipconfig", "/flushdns"],
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
    else:
        subprocess.run(["resolvectl", "flush-caches"], capture_output=True)


def get_blocked_domains(request):
    """GET /api/dns-proxy/blocked-domains/ - Return all blocked domains."""
    if request.method == "GET":
        domains = _load_blocked_domains()
        return JsonResponse({"blocked_domains": domains})
    else:
        return method_not_allowed(request)


@csrf_exempt
def add_blocked_domain(request):
    """POST /api/dns-proxy/blocked-domains/add/ - Add a domain to the block list.

    Body: {"domain": "example.com"}
    """
    if request.method == "POST":
        data = json.loads(request.body)
        domain = data.get("domain", "").strip().lower()
        if not domain:
            return JsonResponse({"error": "domain is required"}, status=400)

        domains = _load_blocked_domains()
        if domain in domains:
            return JsonResponse({"error": "domain already blocked", "blocked_domains": domains}, status=409)

        domains.append(domain)
        _save_blocked_domains(domains)
        _flush_dns_cache()
        return JsonResponse({"status": "success", "blocked_domains": _load_blocked_domains()})
    else:
        return method_not_allowed(request)


@csrf_exempt
def remove_blocked_domain(request):
    """DELETE /api/dns-proxy/blocked-domains/remove/ - Remove a domain from the block list.

    Body: {"domain": "example.com"}
    """
    if request.method == "DELETE":
        data = json.loads(request.body)
        domain = data.get("domain", "").strip().lower()
        if not domain:
            return JsonResponse({"error": "domain is required"}, status=400)

        domains = _load_blocked_domains()
        if domain not in domains:
            return JsonResponse({"error": "domain not found", "blocked_domains": domains}, status=404)

        domains.remove(domain)
        _save_blocked_domains(domains)
        _flush_dns_cache()
        return JsonResponse({"status": "success", "blocked_domains": _load_blocked_domains()})
    else:
        return method_not_allowed(request)
