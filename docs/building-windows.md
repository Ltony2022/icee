# Building the Windows Executable

This guide explains how to package the Electron frontend together with the embedded Django backend into a single Windows installer.

## Prerequisites

- **Python 3.10+** with `pip`. Install backend deps with `pip install -r apps/server/requirements.txt`.
- **PyInstaller** (`pip install pyinstaller`) for generating the backend executable.
- **Node.js 18+** and npm for the Electron/Vite build.
- **Microsoft Visual C++ Build Tools** (CL, Windows SDK) so native modules can compile if needed.
- Enough disk space (≈2 GB) because Electron + PyInstaller outputs are large.

Optionally set `ICEE_PYTHON_PATH` to a custom Python interpreter if `python` is not on your PATH.

## Development workflow

1. In one terminal run the Django backend:
   ```bash
   python apps/server/run_backend.py
   ```
   The API listens on `http://127.0.0.1:8765` by default. Override with `ICEE_BACKEND_PORT`.
2. In `apps/frontend` install deps once: `npm install`.
3. Start the Electron/Vite dev server: `npm run dev`. The main process will automatically spawn the backend script if it is not already running.

## Production build

All commands below are executed from `apps/frontend` unless noted.

1. Ensure backend deps are installed and that `apps/server/dist/backend-service` is either absent or safe to overwrite.
2. Run the unified build:
   ```bash
   npm run build:windows
   ```
   This command invokes `python script/buildExecutable.py`, which:
   - Builds the Django backend via PyInstaller (output in `apps/server/dist/backend-service`).
   - Runs `npm run build:frontend` (TypeScript + Vite + `electron-builder`).
   - Copies Electron installer artifacts to the top-level `release/<version>` folder for easy distribution.
3. Find the Windows installer at `release/<version>/<productName>-Windows-<version>-Setup.exe`.

### Backend-only builds

If you only need to refresh the backend executable (for example before iterating on the frontend), run:
```bash
npm run build:backend
```
This calls `python script/buildExecutable.py --backend-only`, leaving previous Electron artifacts untouched.

## Configuration & environment variables

- `ICEE_BACKEND_PORT`: Port used by the backend (default `8765`). The Electron shell will hit `http://127.0.0.1:<port>`.
- `ICEE_BACKEND_HOST`: Host binding for the backend (default `127.0.0.1`).
- `ICEE_PYTHON_PATH`: Override interpreter for dev builds (Electron main process uses this when spawning the Python script).

## Troubleshooting

- **Backend executable missing inside the installer** – ensure `apps/server/dist/backend-service` exists before running `npm run build:frontend`. The build script handles this automatically when using `npm run build:windows`.
- **Port already in use** – set `ICEE_BACKEND_PORT` before launching Electron or the backend script.
- **Antivirus false positives** – PyInstaller outputs can be flagged. Add the `apps/server/dist` and `release` folders to the AV exclusion list or code-sign the installer.
- **PyInstaller cannot find Django apps** – verify `pip install -r apps/server/requirements.txt` ran in the same interpreter that executes the build script.

Following this workflow guarantees the Windows installer always contains the matching frontend UI and backend API service.








