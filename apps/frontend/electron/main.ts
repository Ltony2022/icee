import { app, BrowserWindow, ipcMain } from "electron";
import { spawn, ChildProcessWithoutNullStreams } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { writeLog, writeCrashReport, setupCrashHandlers, getLogDirectory2 } from "./crashLogger";
import { fileURLToPath } from "node:url";

// const require = createRequire(import.meta.url)
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// The built directory structure
//
// ├─┬─┬ dist
// │ │ └── index.html
// │ │
// │ ├─┬ dist-electron
// │ │ ├── main.js
// │ │ └── preload.mjs
// │
process.env.APP_ROOT = path.join(__dirname, "..");

// 🚧 Use ['ENV_NAME'] avoid vite:define plugin - Vite@2.x
export const VITE_DEV_SERVER_URL = process.env["VITE_DEV_SERVER_URL"];
export const MAIN_DIST = path.join(process.env.APP_ROOT, "dist-electron");
export const RENDERER_DIST = path.join(process.env.APP_ROOT, "dist");

process.env.VITE_PUBLIC = VITE_DEV_SERVER_URL
  ? path.join(process.env.APP_ROOT, "public")
  : RENDERER_DIST;

const isDev = Boolean(VITE_DEV_SERVER_URL);

// todo: remove this if the below works
// const DEFAULT_BACKEND_PORT = process.env.ICEE_BACKEND_PORT || "8765";
const DEFAULT_BACKEND_PORT = process.env.ICEE_BACKEND_PORT || (isDev ? "8000" : "8765");
const DEFAULT_BACKEND_HOST = process.env.ICEE_BACKEND_HOST || "127.0.0.1";

ipcMain.on("icee:get-backend-origin", (event) => {
  const port = process.env.ICEE_BACKEND_PORT || DEFAULT_BACKEND_PORT;
  const host = process.env.ICEE_BACKEND_HOST || DEFAULT_BACKEND_HOST;
  event.returnValue = `http://${host}:${port}`;
});

let win: BrowserWindow | null;
let backendProcess: ChildProcessWithoutNullStreams | null = null;

// const isDev = Boolean(VITE_DEV_SERVER_URL);

function getDevBackendCommand() {
  const pythonBinary = process.env.ICEE_PYTHON_PATH || "python";
  const backendScript = path.join(process.env.APP_ROOT, "..", "server", "run_backend.py");
  return { command: pythonBinary, args: [backendScript], cwd: path.dirname(backendScript) };
}

function getProductionBackendCommand() {
  const resourcesBackendDir = path.join(process.resourcesPath, "backend-service");
  const executableName = process.platform === "win32" ? "backend-service.exe" : "backend-service";
  const executablePath = path.join(resourcesBackendDir, executableName);

  if (!fs.existsSync(executablePath)) {
    const error = new Error(`Backend executable missing at ${executablePath}`);
    writeCrashReport("electron-main", error, { executablePath, resourcesBackendDir });
    throw error;
  }

  return { command: executablePath, args: [], cwd: resourcesBackendDir };
}

function startBackend() {
  if (backendProcess) {
    return backendProcess;
  }

  const { command, args, cwd } = isDev ? getDevBackendCommand() : getProductionBackendCommand();
  backendProcess = spawn(command, args, {
    cwd,
    env: {
      ...process.env,
      ICEE_BACKEND_PORT: DEFAULT_BACKEND_PORT,
      ICEE_BACKEND_HOST: DEFAULT_BACKEND_HOST,
      ICEE_CRASH_LOG_DIR: getLogDirectory2(),
    },
    windowsHide: true,
  });

  backendProcess.stdout.on("data", (data) => {
    const message = data.toString().trim();
    console.log(`[backend] ${message}`);
    writeLog("INFO", "backend", message);
  });
  backendProcess.stderr.on("data", (data) => {
    const message = data.toString().trim();
    console.error(`[backend] ${message}`);
    writeLog("ERROR", "backend", message);
  });
  backendProcess.on("exit", (code, signal) => {
    const exitInfo = `Backend process exited with code ${code ?? "unknown"}, signal ${signal ?? "none"}`;
    console.log(exitInfo);
    writeLog("WARN", "backend", exitInfo);

    if (code !== 0 && code !== null) {
      writeCrashReport("backend", new Error(`Backend crashed with exit code ${code}`), {
        exitCode: code,
        signal: signal,
        command: command,
        args: args,
        cwd: cwd,
      });
    }

    backendProcess = null;
    if (!isDev && code !== 0) {
      app.quit();
    }
  });

  return backendProcess;
}

function stopBackend() {
  if (backendProcess) {
    backendProcess.removeAllListeners();
    backendProcess.kill();
    backendProcess = null;
  }
}

function createWindow() {
  win = new BrowserWindow({
    icon: path.join(process.env.VITE_PUBLIC, "electron-vite.svg"),
    webPreferences: {
      preload: path.join(__dirname, "preload.mjs"),
    },
    minWidth: 1024,
    // specify width upon window creation
    width: 1024,
  });

  // Test active push message to Renderer-process.
  win.webContents.on("did-finish-load", () => {
    win?.webContents.send("main-process-message", new Date().toLocaleString());
  });

  if (VITE_DEV_SERVER_URL) {
    win.loadURL(VITE_DEV_SERVER_URL);
  } else {
    // win.loadFile('dist/index.html')
    win.loadFile(path.join(RENDERER_DIST, "index.html"), { hash: "/" });
  }
}

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
    win = null;
  }
});

app.on("activate", () => {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

app.whenReady().then(() => {
  setupCrashHandlers();
  writeLog("INFO", "electron-main", `App started. Log directory: ${getLogDirectory2()}`);
  startBackend();
  createWindow();
});

app.on("before-quit", () => {
  writeLog("INFO", "electron-main", "App quitting");
  stopBackend();
});
