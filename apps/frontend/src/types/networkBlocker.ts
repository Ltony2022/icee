/**
 * Represents the current status of a blocked website
 */
export type BlockStatus = "Active" | "Paused" | "Expired";

/**
 * Represents the blocking method used for a website
 */
export type BlockMethod = "DNS" | "Hosts File" | "Firewall";

/**
 * Main data model for a blocked website entry
 */
export interface BlockedWebsite {
  id: string;
  websiteName: string;
  status: BlockStatus;
  blockMethod: BlockMethod;
  remainingTime: number | null; // in minutes, null means permanent
  createdAt: Date;
  expiresAt: Date | null;
}

/**
 * Form data for adding/editing a blocked website
 */
export interface BlockWebsiteFormData {
  websiteName: string;
  blockMethod: BlockMethod;
  duration: number | null; // in minutes, null means permanent
}

/**
 * DNS proxy running status from backend
 */
export interface ProxyStatus {
  running: boolean;
  pid?: number;
}

/**
 * Configuration for starting the DNS proxy
 */
export interface ProxyConfig {
  listen_host?: string;
  listen_port?: number;
  upstream_host?: string;
  upstream_port?: number;
  timeout?: number;
  log_level?: string;
}
