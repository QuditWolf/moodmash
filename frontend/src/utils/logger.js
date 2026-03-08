/**
 * Frontend Logging Utility
 * 
 * Provides structured logging for the frontend application.
 * Logs to console in development and can be extended for production logging.
 */

const LOG_LEVELS = {
  DEBUG: 'DEBUG',
  INFO: 'INFO',
  WARN: 'WARN',
  ERROR: 'ERROR',
};

/**
 * Get current environment
 */
const isDevelopment = import.meta.env.MODE === 'development';

/**
 * Format log message with timestamp and context
 */
const formatLogMessage = (level, message, context = {}) => {
  const timestamp = new Date().toISOString();
  return {
    timestamp,
    level,
    message,
    context,
    environment: import.meta.env.MODE,
  };
};

/**
 * Filter sensitive data from context
 */
const filterSensitiveData = (context) => {
  const sensitive = ['token', 'password', 'authorization', 'secret', 'apiKey'];
  const filtered = { ...context };
  
  Object.keys(filtered).forEach(key => {
    if (sensitive.some(s => key.toLowerCase().includes(s))) {
      filtered[key] = '[REDACTED]';
    }
  });
  
  return filtered;
};

/**
 * Logger class for structured logging
 */
class Logger {
  constructor(name) {
    this.name = name;
  }

  /**
   * Log debug message
   */
  debug(message, context = {}) {
    if (isDevelopment) {
      const filteredContext = filterSensitiveData(context);
      const logData = formatLogMessage(LOG_LEVELS.DEBUG, message, {
        logger: this.name,
        ...filteredContext,
      });
      console.debug(`[${logData.timestamp}] [${this.name}] ${message}`, logData.context);
    }
  }

  /**
   * Log info message
   */
  info(message, context = {}) {
    const filteredContext = filterSensitiveData(context);
    const logData = formatLogMessage(LOG_LEVELS.INFO, message, {
      logger: this.name,
      ...filteredContext,
    });
    console.info(`[${logData.timestamp}] [${this.name}] ${message}`, logData.context);
  }

  /**
   * Log warning message
   */
  warn(message, context = {}) {
    const filteredContext = filterSensitiveData(context);
    const logData = formatLogMessage(LOG_LEVELS.WARN, message, {
      logger: this.name,
      ...filteredContext,
    });
    console.warn(`[${logData.timestamp}] [${this.name}] ${message}`, logData.context);
  }

  /**
   * Log error message
   */
  error(message, error = null, context = {}) {
    const filteredContext = filterSensitiveData(context);
    const logData = formatLogMessage(LOG_LEVELS.ERROR, message, {
      logger: this.name,
      error: error ? {
        name: error.name,
        message: error.message,
        stack: isDevelopment ? error.stack : undefined,
      } : undefined,
      ...filteredContext,
    });
    console.error(`[${logData.timestamp}] [${this.name}] ${message}`, logData.context);
  }

  /**
   * Log API request
   */
  logApiRequest(method, url, status, duration, context = {}) {
    const filteredContext = filterSensitiveData(context);
    this.info(`API ${method} ${url} - ${status}`, {
      method,
      url,
      status,
      duration_ms: duration,
      ...filteredContext,
    });
  }

  /**
   * Log API error
   */
  logApiError(method, url, error, context = {}) {
    const filteredContext = filterSensitiveData(context);
    this.error(`API ${method} ${url} failed`, error, {
      method,
      url,
      error_type: error?.name,
      error_message: error?.message,
      ...filteredContext,
    });
  }
}

/**
 * Get logger instance
 */
export const getLogger = (name) => {
  return new Logger(name);
};

/**
 * Default logger instance
 */
export const logger = new Logger('app');

export default logger;
