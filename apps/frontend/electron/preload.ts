import { ipcRenderer, contextBridge } from "electron";

function readBackendOriginFromMain(): string {
  try {
    const v = ipcRenderer.sendSync("icee:get-backend-origin") as unknown;
    if (typeof v === "string" && v.startsWith("http")) {
      return v.replace(/\/$/, "");
    }
  } catch {
    // Not running under Electron
  }
  // this is the fallback - todo: remove the current line if below works
  // return 'http://127.0.0.1:8765'
  return import.meta.env.DEV
    ? "http://127.0.0.1:8000"
    : "http://127.0.0.1:8765";
}

contextBridge.exposeInMainWorld("icee", {
  backendOrigin: readBackendOriginFromMain(),
});

// --------- Expose some API to the Renderer process ---------
contextBridge.exposeInMainWorld("ipcRenderer", {
  on(...args: Parameters<typeof ipcRenderer.on>) {
    const [channel, listener] = args;
    return ipcRenderer.on(channel, (event, ...args) =>
      listener(event, ...args),
    );
  },
  off(...args: Parameters<typeof ipcRenderer.off>) {
    const [channel, ...omit] = args;
    return ipcRenderer.off(channel, ...omit);
  },
  send(...args: Parameters<typeof ipcRenderer.send>) {
    const [channel, ...omit] = args;
    return ipcRenderer.send(channel, ...omit);
  },
  invoke(...args: Parameters<typeof ipcRenderer.invoke>) {
    const [channel, ...omit] = args;
    return ipcRenderer.invoke(channel, ...omit);
  },

  // You can expose other APTs you need here.
  // ...
});
