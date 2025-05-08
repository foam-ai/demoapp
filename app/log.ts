export enum LogLevel {
    DEBUG,
    INFO,
    WARN,
    ERROR
  }
  
  export class Logger {
    constructor(private context: string) {}
  
    log(level: LogLevel, message: string, ...data: any[]): void {
      const timestamp = new Date().toISOString();
      console.log(`[${timestamp}] [${LogLevel[level]}] [${this.context}]: ${message}`, ...data);
    }
  
    debug(message: string, ...data: any[]): void {
      this.log(LogLevel.DEBUG, message, ...data);
    }
  
    info(message: string, ...data: any[]): void {
      this.log(LogLevel.INFO, message, ...data);
    }
  
    warn(message: string, ...data: any[]): void {
      this.log(LogLevel.WARN, message, ...data);
    }
  
    error(message: string, ...data: any[]): void {
      this.log(LogLevel.ERROR, message, ...data);
    }
  }
  