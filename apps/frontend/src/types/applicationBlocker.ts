export interface BlockedApplication {
  name: string;
  blocked: boolean;
}

export interface BlockedApplicationResponse {
  blocked_applications: BlockedApplication[];
}

export interface ApplicationMutationResponse {
  status: string;
  applications: BlockedApplication[];
}

export interface InstalledApplication {
  display_name: string;
  executable: string;
}

export interface InstalledApplicationsResponse {
  installed_applications: InstalledApplication[];
}
