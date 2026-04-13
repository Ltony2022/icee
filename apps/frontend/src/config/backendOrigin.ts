const DEFAULT_HOST = "127.0.0.1";

/**
 * Base URL for the Django API.
 * - Electron: `window.icee.backendOrigin` from main (ICEE_BACKEND_*); VITE_ vars are not required.
 * - Vite only: if no `VITE_ICEE_*` is set at build time, falls back to 127.0.0.1 and port 8000 (dev) or 8765 (production build).
 */
export function getBackendOrigin(): string {
  if (typeof window !== "undefined" && window.icee?.backendOrigin) {
    return window.icee.backendOrigin;
  }

  const explicit = import.meta.env.VITE_ICEE_BACKEND_ORIGIN;
  if (explicit) {
    return explicit.replace(/\/$/, "");
  }

  const host = import.meta.env.VITE_ICEE_BACKEND_HOST ?? DEFAULT_HOST;
  const defaultPort = import.meta.env.DEV ? "8000" : "8765";
  const port = import.meta.env.VITE_ICEE_BACKEND_PORT ?? defaultPort;
  return `http://${host}:${port}`;
}
