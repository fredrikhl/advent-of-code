#include "log.h"


/**
 * Verbosity level to text conversion.
 *
 * Example:
 *   log_verbosity_prefix[LOG_DEBUG];
 */
const char * const log_verbosity_prefix[] = {"ERROR", "WARN", "INFO", "DEBUG"};


/**
 * Current/initial verbosity level
 *
 * Should be changed with log_set_level(<enum verbosity>);
 */
enum verbosity log_current_level = LOG_DEFAULT;


/**
 * Set global verbosity level
 *
 * Example:
 *   log_set_level(LOG_INFO);
 */
enum verbosity log_set_level(enum verbosity level)
{
    int old_level = log_current_level;
    log_current_level = level;
    return old_level;
}


/**
 * Log to stderr with an appropriate prefix.
 *
 * Examples:
 *   log_with_level(LOG_DEBUG, "some-value='%s'", "value");
 *   log_with_level(LOG_ERROR, "something went wrong (errno: %d)", 3);
 */
void log_with_level(enum verbosity log_level, char * fmt, ...)
{
    va_list args;
    const char * prefix;

    if (log_level > log_current_level) {
        return;
    }

    if (log_level > LOG_DEBUG) {
        prefix = log_verbosity_prefix[LOG_DEBUG];
    } else if (log_level < LOG_ERROR) {
        prefix = log_verbosity_prefix[LOG_ERROR];
    } else {
        prefix = log_verbosity_prefix[log_level];
    }

    fprintf(stderr, "%s: ", prefix);
    va_start(args, fmt);
    vfprintf(stderr, fmt, args);
    va_end(args);
    fprintf(stderr, "\n");
}
