#!/usr/bin/env python
"""
Export crash logs from the icee-utils application.

This script collects crash logs from known locations and exports them
to a single directory or zip file for debugging purposes.
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import sys
from datetime import datetime
from pathlib import Path


def get_electron_crash_log_dir() -> Path | None:
    """Get the Electron app's crash log directory based on platform."""
    system = platform.system()

    if system == "Windows":
        app_data = os.environ.get("APPDATA")
        if app_data:
            # Electron uses the app name from package.json
            possible_paths = [
                Path(app_data) / "icee-utils" / "crash-logs",
                Path(app_data) / "icee-utils-private" / "crash-logs",
                Path(app_data) / "Electron" / "crash-logs",
            ]
            for p in possible_paths:
                if p.exists():
                    return p
    elif system == "Darwin":  # macOS
        home = Path.home()
        possible_paths = [
            home / "Library" / "Application Support" / "icee-utils" / "crash-logs",
            home / "Library" / "Application Support" / "icee-utils-private" / "crash-logs",
        ]
        for p in possible_paths:
            if p.exists():
                return p
    elif system == "Linux":
        config_home = os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))
        possible_paths = [
            Path(config_home) / "icee-utils" / "crash-logs",
            Path(config_home) / "icee-utils-private" / "crash-logs",
        ]
        for p in possible_paths:
            if p.exists():
                return p

    return None


def get_backend_crash_log_dir() -> Path | None:
    """Get the backend's crash log directory."""
    script_dir = Path(__file__).resolve().parent
    root_dir = script_dir.parent

    possible_paths = [
        root_dir / "apps" / "server" / "crash-logs",
        root_dir / "crash-logs",
    ]

    for p in possible_paths:
        if p.exists():
            return p

    return None


def collect_log_files(log_dir: Path) -> list[Path]:
    """Collect all log and crash report files from a directory."""
    files = []
    if not log_dir.exists():
        return files

    patterns = ["*.log", "*.txt", "crash-*"]
    for pattern in patterns:
        files.extend(log_dir.glob(pattern))

    return sorted(set(files), key=lambda f: f.stat().st_mtime, reverse=True)


def export_logs(output_path: Path, as_zip: bool = False) -> None:
    """Export all crash logs to the specified location."""
    electron_dir = get_electron_crash_log_dir()
    backend_dir = get_backend_crash_log_dir()

    print("Searching for crash logs...")
    print(f"  Electron logs: {electron_dir or 'Not found'}")
    print(f"  Backend logs: {backend_dir or 'Not found'}")

    all_files: list[tuple[Path, str]] = []

    if electron_dir:
        for f in collect_log_files(electron_dir):
            all_files.append((f, f"electron/{f.name}"))

    if backend_dir:
        for f in collect_log_files(backend_dir):
            all_files.append((f, f"backend/{f.name}"))

    if not all_files:
        print("\nNo crash logs found.")
        return

    print(f"\nFound {len(all_files)} log file(s)")

    if as_zip:
        # Export as zip
        zip_path = output_path.with_suffix(".zip")
        temp_dir = output_path.parent / f"_temp_export_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        temp_dir.mkdir(parents=True, exist_ok=True)

        try:
            for src, rel_path in all_files:
                dest = temp_dir / rel_path
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)

            shutil.make_archive(str(output_path.with_suffix("")), "zip", temp_dir)
            print(f"\nExported to: {zip_path}")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    else:
        # Export as directory
        output_path.mkdir(parents=True, exist_ok=True)

        for src, rel_path in all_files:
            dest = output_path / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            print(f"  Copied: {rel_path}")

        print(f"\nExported to: {output_path}")


def list_logs() -> None:
    """List all available crash logs without exporting."""
    electron_dir = get_electron_crash_log_dir()
    backend_dir = get_backend_crash_log_dir()

    print("Crash Log Locations:")
    print(f"  Electron: {electron_dir or 'Not found'}")
    print(f"  Backend: {backend_dir or 'Not found'}")
    print()

    if electron_dir:
        files = collect_log_files(electron_dir)
        if files:
            print(f"Electron logs ({len(files)} files):")
            for f in files[:10]:
                size = f.stat().st_size
                mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                print(f"  {f.name} ({size} bytes, {mtime})")
            if len(files) > 10:
                print(f"  ... and {len(files) - 10} more")
            print()

    if backend_dir:
        files = collect_log_files(backend_dir)
        if files:
            print(f"Backend logs ({len(files)} files):")
            for f in files[:10]:
                size = f.stat().st_size
                mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                print(f"  {f.name} ({size} bytes, {mtime})")
            if len(files) > 10:
                print(f"  ... and {len(files) - 10} more")


def read_latest_crash() -> None:
    """Read and display the contents of the most recent crash report."""
    electron_dir = get_electron_crash_log_dir()
    backend_dir = get_backend_crash_log_dir()

    crash_files: list[Path] = []

    if electron_dir:
        crash_files.extend(electron_dir.glob("crash-*.txt"))
    if backend_dir:
        crash_files.extend(backend_dir.glob("crash-*.txt"))

    if not crash_files:
        print("No crash reports found.")
        return

    latest = max(crash_files, key=lambda f: f.stat().st_mtime)
    print(f"Latest crash report: {latest}")
    print("=" * 60)
    print(latest.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export crash logs from icee-utils application."
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available crash logs without exporting.",
    )
    parser.add_argument(
        "--latest", "-L",
        action="store_true",
        help="Display the contents of the latest crash report.",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=Path.cwd() / f"crash-export-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        help="Output path for exported logs (default: ./crash-export-<timestamp>).",
    )
    parser.add_argument(
        "--zip", "-z",
        action="store_true",
        help="Export as a zip file instead of a directory.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.list:
        list_logs()
    elif args.latest:
        read_latest_crash()
    else:
        export_logs(args.output, as_zip=args.zip)


if __name__ == "__main__":
    main()
