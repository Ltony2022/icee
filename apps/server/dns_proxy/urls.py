from django.urls import path

from dns_proxy.api.blocked_domains import get_blocked_domains, add_blocked_domain, remove_blocked_domain
from dns_proxy.api.proxy_control import get_proxy_status, start_proxy, stop_proxy
from dns_proxy.api.dns_logs import get_dns_logs, clear_dns_logs

urlpatterns = [
    # Blocked domains management
    path("blocked-domains/", get_blocked_domains),
    path("blocked-domains/add/", add_blocked_domain),
    path("blocked-domains/remove/", remove_blocked_domain),

    # Proxy control
    path("status/", get_proxy_status),
    path("start/", start_proxy),
    path("stop/", stop_proxy),

    # DNS logs
    path("logs/", get_dns_logs),
    path("logs/clear/", clear_dns_logs),
]
