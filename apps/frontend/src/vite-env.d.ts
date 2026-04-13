/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** Full API origin, e.g. http://127.0.0.1:8000 when using `manage.py runserver` */
  readonly VITE_ICEE_BACKEND_ORIGIN?: string;
  readonly VITE_ICEE_BACKEND_HOST?: string;
  readonly VITE_ICEE_BACKEND_PORT?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

interface Window {
  icee?: {
    backendOrigin: string;
  };
}
