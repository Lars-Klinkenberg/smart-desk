export enum LogLevel {
  'DEBUG',
  'INFO',
  'WARNING',
  'ERROR',
  'CRITICAL',
}

export interface Log {
  id: string;
  log_level: LogLevel;
  message: string;
  service_name: string;
  timestamp: Date;
}

export enum LogSource {
    DESK_CONTROLLER = "desk_controller",
    API = "api",
    DAILY_JOB = "jobs/daily",
    MONTHLY_JOB = "jobs/monthly"
}