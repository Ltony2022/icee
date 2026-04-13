#!/usr/bin/env python
"""
Utility entrypoint that prepares the Django project and serves it via waitress.

The script is intended to be frozen with PyInstaller so it must avoid relying
on shell wrappers or virtualenv activation. It handles migrations on startup
and binds to a predictable localhost port that the Electron shell can target.
"""

from __future__ import annotations

import logging
import os
import runpy
import signal
import sys
import traceback
from datetime import datetime
from pathlib import Path

from waitress import serve


def get_base_path() -> Path:
    """Get base path - handles both normal and PyInstaller frozen execution."""
    if getattr(sys, "frozen", False):
        # Running as compiled executable
        return Path(sys.executable).parent
    else:
        # Running as script
        return Path(__file__).resolve().parent


IS_FROZEN = bool(getattr(sys, "frozen", False))
BASE_PATH = get_base_path()
ROOT_DIR = BASE_PATH.parent.parent if not IS_FROZEN else BASE_PATH
SERVER_DIR = (
    ROOT_DIR / "apps" / "server" if not IS_FROZEN else BASE_PATH
)
SRC_DIR = ROOT_DIR / "src" if not IS_FROZEN else BASE_PATH
DEFAULT_PORT = int(os.environ.get("ICEE_BACKEND_PORT", "8765"))

logger = logging.getLogger(__name__)


def get_crash_log_dir() -> Path:
    """Get the crash log directory. Uses ICEE_CRASH_LOG_DIR env var or falls back."""
    crash_dir = os.environ.get("ICEE_CRASH_LOG_DIR")
    if crash_dir:
        log_dir = Path(crash_dir)
    else:
        # When frozen, use the executable's directory
        if getattr(sys, "frozen", False):
            log_dir = BASE_PATH / "crash-logs"
        else:
            log_dir = SERVER_DIR / "crash-logs"

    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        # Fallback to temp directory
        import tempfile

        log_dir = Path(tempfile.gettempdir()) / "icee-utils-crash-logs"
        log_dir.mkdir(parents=True, exist_ok=True)

    return log_dir


def write_crash_report(error: Exception, context: str = "") -> Path:
    """Write a crash report to disk and return the file path."""
    log_dir = get_crash_log_dir()
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    crash_file = log_dir / f"crash-backend-{timestamp}.txt"

    report_lines = [
        "CRASH REPORT",
        "============",
        "",
        f"Timestamp: {datetime.now().isoformat()}",
        f"Source: backend (Python)",
        f"Python Version: {sys.version}",
        f"Platform: {sys.platform}",
        "",
        "ERROR",
        "-----",
        f"Type: {type(error).__name__}",
        f"Message: {str(error)}",
        "",
        "TRACEBACK",
        "---------",
        traceback.format_exc(),
    ]

    if context:
        report_lines.extend(
            [
                "",
                "CONTEXT",
                "-------",
                context,
            ]
        )

    crash_file.write_text("\n".join(report_lines), encoding="utf-8")
    return crash_file


def configure_pythonpath() -> None:
    """Ensure Django and helper packages are importable when frozen."""
    APPS_DIR = SERVER_DIR.parent
    for path in {APPS_DIR, ROOT_DIR, SERVER_DIR, SRC_DIR}:
        if path.exists() and str(path) not in sys.path:
            sys.path.insert(0, str(path))


def resolve_dns_proxy_script() -> Path:
    """Resolve the DNS worker script location for script and frozen runs."""
    candidates: list[Path] = []
    if IS_FROZEN:
        candidates.append(BASE_PATH / "proxy" / "dns_proxy.py")
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            candidates.append(Path(meipass) / "proxy" / "dns_proxy.py")
    else:
        candidates.append(ROOT_DIR / "proxy" / "dns_proxy.py")

    for path in candidates:
        if path.exists():
            return path
    return candidates[0]


def maybe_run_dns_proxy_worker() -> bool:
    """Run the DNS worker mode and stop normal backend boot if requested."""
    if len(sys.argv) < 2 or sys.argv[1] != "--dns-proxy-worker":
        return False

    script_path = resolve_dns_proxy_script()
    if not script_path.exists():
        raise FileNotFoundError(f"DNS proxy worker script not found: {script_path}")

    # Forward all remaining args to proxy/dns_proxy.py.
    sys.argv = [str(script_path), *sys.argv[2:]]
    runpy.run_path(str(script_path), run_name="__main__")
    return True


def configure_env() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    os.environ.setdefault("DJANGO_COLORS", "dark")


def apply_migrations() -> None:
    """Run migrations (silently) so the embedded DB is up to date."""
    from django.core.management import call_command

    call_command("migrate", interactive=False, run_syncdb=True, verbosity=0)


def start_server() -> None:
    """Start the WSGI application with waitress."""
    from django.core.wsgi import get_wsgi_application

    host = os.environ.get("ICEE_BACKEND_HOST", "127.0.0.1")
    port = int(os.environ.get("ICEE_BACKEND_PORT", DEFAULT_PORT))
    logging.info("Serving Django backend on http://%s:%s", host, port)
    serve(get_wsgi_application(), listen=f"{host}:{port}")


def main() -> None:
    logging.basicConfig(
        level=os.environ.get("ICEE_BACKEND_LOGLEVEL", "INFO"),
        format="[%(asctime)s] %(levelname)s %(message)s",
    )

    try:
        logging.info("Crash logs will be saved to: %s", get_crash_log_dir())

        configure_pythonpath()
        configure_env()

        import django

        django.setup()
        apply_migrations()
        start_server()
    except Exception as e:
        crash_file = write_crash_report(
            e, context="Error during backend startup or runtime"
        )
        logger.critical("Backend crashed. Crash report written to: %s", crash_file)
        print(f"[CRASH] Backend crashed. Report: {crash_file}", file=sys.stderr)
        raise


if __name__ == "__main__":
    if maybe_run_dns_proxy_worker():
        sys.exit(0)

    # Ensure Ctrl+C stops waitress promptly.
    signal.signal(signal.SIGINT, lambda *_: sys.exit(0))
    main()
