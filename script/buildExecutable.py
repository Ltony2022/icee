"""
Utility build script that prepares distributable artifacts for the icee-utils app.

For now it focuses on compiling the Django backend into a standalone executable
via PyInstaller. Later steps in the plan will extend this script to orchestrate
the Electron build as well, so the CLI has been structured with that in mind.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SERVER_DIR = ROOT_DIR / "apps" / "server"
FRONTEND_DIR = ROOT_DIR / "apps" / "frontend"
SPEC_PATH = SERVER_DIR / "backend.spec"
DIST_DIR = SERVER_DIR / "dist"
RELEASE_DIR = ROOT_DIR / "release"
REQUIREMENTS_FILE = SERVER_DIR / "requirements.txt"


def check_prerequisites() -> None:
    try:
        import PyInstaller  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover - CLI guard
        raise SystemExit(
            "PyInstaller is required. Install it with `pip install pyinstaller`."
        ) from exc


def ensure_backend_dependencies() -> None:
    """Install backend runtime requirements (waitress, Django, etc.)."""
    if not REQUIREMENTS_FILE.exists():
        raise SystemExit(f"Missing requirements file: {REQUIREMENTS_FILE}")

    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)],
        check=True,
    )


def run_backend_build(clean: bool = True) -> None:
    if clean and DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)

    cmd = ["pyinstaller", "--noconfirm", "--clean", str(SPEC_PATH)]
    subprocess.run(cmd, cwd=SERVER_DIR, check=True)  # pragma: no cover


def run_frontend_build() -> None:
    cmd = ["npm", "run", "build:frontend"]
    subprocess.run(
        cmd, cwd=FRONTEND_DIR, check=True, shell=(sys.platform == "win32")
    )  # pragma: no cover


def clean_node_modules() -> None:
    """Remove node_modules folder to reduce distribution size."""
    node_modules_dir = FRONTEND_DIR / "node_modules"
    if node_modules_dir.exists():
        print(f"Removing {node_modules_dir}...")
        shutil.rmtree(node_modules_dir)
        print("node_modules removed successfully.")


def read_frontend_version() -> str:
    package_json = FRONTEND_DIR / "package.json"
    with open(package_json, encoding="utf-8") as handle:
        package = json.load(handle)
    return str(package.get("version", "0.0.0"))


def copy_release_artifacts(version: str) -> None:
    source_dir = FRONTEND_DIR / "release" / version
    if not source_dir.exists():
        raise FileNotFoundError(
            f"Electron release not found at {source_dir}. Did the build succeed?"
        )

    target_dir = RELEASE_DIR / version
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_dir, target_dir)
    print(f"Installer artifacts copied to {target_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build project executables.")
    parser.add_argument(
        "--backend-only",
        action="store_true",
        help="Only build the backend PyInstaller distribution.",
    )
    parser.add_argument(
        "--skip-backend-clean",
        action="store_true",
        help="Keep the existing backend dist/ folder instead of deleting it.",
    )
    parser.add_argument(
        "--skip-release-copy",
        action="store_true",
        help="Skip copying frontend release artifacts to the top-level release/ folder.",
    )
    parser.add_argument(
        "--clean-node-modules",
        action="store_true",
        help="Remove node_modules folder after the frontend build completes.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    check_prerequisites()

    # Ensure waitress and other backend deps are present before freezing.
    ensure_backend_dependencies()

    run_backend_build(clean=not args.skip_backend_clean)

    if args.backend_only:
        print("Backend build completed.")
        return

    run_frontend_build()

    if args.clean_node_modules:
        clean_node_modules()

    if not args.skip_release_copy:
        version = read_frontend_version()
        copy_release_artifacts(version)


if __name__ == "__main__":
    main()
