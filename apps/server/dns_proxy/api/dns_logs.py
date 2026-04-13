from pathlib import Path

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from src.core.exception.django_exception import method_not_allowed


PROXY_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent / "proxy"
LOG_FILE = PROXY_DIR / "dns_proxy.log"


def get_dns_logs(request):
    """GET /api/dns-proxy/logs/ - Return recent DNS proxy log entries.

    Query params:
        lines (int): Number of most recent lines to return (default 100, max 1000).
    """
    if request.method == "GET":
        max_lines = min(int(request.GET.get("lines", 100)), 1000)

        if not LOG_FILE.exists():
            return JsonResponse({"logs": [], "total_lines": 0})

        all_lines = LOG_FILE.read_text(encoding="utf-8").splitlines()
        recent = all_lines[-max_lines:]

        return JsonResponse({
            "logs": recent,
            "total_lines": len(all_lines),
            "returned_lines": len(recent),
        })
    else:
        return method_not_allowed(request)


@csrf_exempt
def clear_dns_logs(request):
    """DELETE /api/dns-proxy/logs/clear/ - Clear the DNS proxy log file."""
    if request.method == "DELETE":
        if LOG_FILE.exists():
            LOG_FILE.write_text("", encoding="utf-8")
        return JsonResponse({"status": "cleared"})
    else:
        return method_not_allowed(request)
