import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { app } from "electron";

const MAX_LOG_SIZE = 5 * 1024 * 1024; // 5MB
const MAX_LOG_FILES = 5;

let logFilePath: string | null = null;
let crashLogDir: string | null = null;

function tryInstallationLogDir(): string | null {
  try {
    if (!app.isPackaged) return null;
    const exeDir = path.dirname(app.getPath("exe"));
    const target = path.join(exeDir, "logs");
    fs.mkdirSync(target, { recursive: true });
    return target;
  } catch {
    return null;
  }
}

function getLogDirectory(): string {
  if (crashLogDir) return crashLogDir;

  // Prefer a logs folder next to the installed executable (requested behavior).
  const installDir = tryInstallationLogDir();
  if (installDir) {
    crashLogDir = installDir;
    return crashLogDir;
  }

  try {
    const userDataPath = app.getPath("userData");
    crashLogDir = path.join(userDataPath, "crash-logs");
  } catch {
    crashLogDir = path.join(os.tmpdir(), "icee-utils-crash-logs");
  }

  try {
    if (!fs.existsSync(crashLogDir)) {
      fs.mkdirSync(crashLogDir, { recursive: true });
    }
  } catch {
    crashLogDir = os.tmpdir();
  }

  return crashLogDir;
}

function getLogFilePath(): string {
  if (logFilePath) return logFilePath;

  const logDir = getLogDirectory();
  const date = new Date().toISOString().split("T")[0];
  logFilePath = path.join(logDir, `icee-${date}.log`);

  return logFilePath;
}

function rotateLogsIfNeeded(): void {
  try {
    const filePath = getLogFilePath();

    if (!fs.existsSync(filePath)) return;

    const stats = fs.statSync(filePath);
    if (stats.size < MAX_LOG_SIZE) return;

    const logDir = getLogDirectory();
    const baseName = path.basename(filePath, ".log");

    for (let i = MAX_LOG_FILES - 1; i >= 1; i--) {
      const oldPath = path.join(logDir, `${baseName}.${i}.log`);
      const newPath = path.join(logDir, `${baseName}.${i + 1}.log`);
      if (fs.existsSync(oldPath)) {
        if (i === MAX_LOG_FILES - 1) {
          fs.unlinkSync(oldPath);
        } else {
          fs.renameSync(oldPath, newPath);
        }
      }
    }

    fs.renameSync(filePath, path.join(logDir, `${baseName}.1.log`));
    logFilePath = null;
  } catch {
    // Ignore rotation errors
  }
}

function formatTimestamp(): string {
  return new Date().toISOString();
}

export function writeLog(level: string, source: string, message: string): void {
  try {
    rotateLogsIfNeeded();
    const filePath = getLogFilePath();
    const logLine = `[${formatTimestamp()}] [${level}] [${source}] ${message}\n`;
    fs.appendFileSync(filePath, logLine);
  } catch (err) {
    console.error("Failed to write log:", err);
  }
}

export function writeCrashReport(
  source: string,
  error: Error | string,
  additionalInfo?: Record<string, unknown>
): string {
  const logDir = getLogDirectory();
  const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
  const crashFilePath = path.join(logDir, `crash-${source}-${timestamp}.txt`);

  const errorMessage =
    error instanceof Error ? error.stack || error.message : String(error);

  let report = `CRASH REPORT\n`;
  report += `============\n\n`;
  report += `Timestamp: ${new Date().toISOString()}\n`;
  report += `Source: ${source}\n`;
  report += `Platform: ${process.platform}\n`;
  report += `Arch: ${process.arch}\n`;
  report += `Node Version: ${process.version}\n`;
  report += `Electron Version: ${process.versions.electron || "N/A"}\n`;
  report += `Log Directory: ${logDir}\n\n`;
  report += `ERROR\n`;
  report += `-----\n`;
  report += `${errorMessage}\n\n`;

  if (additionalInfo) {
    report += `ADDITIONAL INFO\n`;
    report += `---------------\n`;
    for (const [key, value] of Object.entries(additionalInfo)) {
      try {
        report += `${key}: ${JSON.stringify(value, null, 2)}\n`;
      } catch {
        report += `${key}: [unserializable]\n`;
      }
    }
    report += `\n`;
  }

  try {
    fs.writeFileSync(crashFilePath, report, { flag: "w" });
    console.error(`[CRASH] Report written to: ${crashFilePath}`);
  } catch (err) {
    console.error("Failed to write crash report:", err);
    // Try writing to stderr at least
    console.error("Crash report content:\n", report);
  }

  return crashFilePath;
}

export function setupCrashHandlers(): void {
  // Handle uncaught exceptions
  process.on("uncaughtException", (error, origin) => {
    console.error(`[CRASH] Uncaught exception from ${origin}:`, error);
    writeLog(
      "FATAL",
      "electron-main",
      `Uncaught exception (${origin}): ${error.stack || error.message}`
    );
    writeCrashReport("electron-main", error, { origin });

    // Give time for file write, then exit
    setTimeout(() => process.exit(1), 100);
  });

  // Handle unhandled promise rejections
  process.on("unhandledRejection", (reason) => {
    const message =
      reason instanceof Error ? reason.stack || reason.message : String(reason);
    console.error("[CRASH] Unhandled rejection:", message);
    writeLog("ERROR", "electron-main", `Unhandled rejection: ${message}`);
    writeCrashReport(
      "electron-main",
      reason instanceof Error ? reason : new Error(String(reason)),
      { type: "unhandledRejection" }
    );
  });

  writeLog("INFO", "electron-main", "Crash handlers initialized");
  console.log(`[LOG] Crash logs will be saved to: ${getLogDirectory()}`);
}

export function getLogDirectory2(): string {
  return getLogDirectory();
}
