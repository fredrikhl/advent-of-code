#pragma once

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LOG_DEFAULT LOG_ERROR

enum verbosity{LOG_ERROR, LOG_WARNING, LOG_INFO, LOG_DEBUG};

enum verbosity log_set_level(enum verbosity level);
void log_with_level(enum verbosity log_level, char * fmt, ...);

#define log_debug(...) log_with_level(LOG_DEBUG, __VA_ARGS__);
#define log_info(...) log_with_level(LOG_INFO, __VA_ARGS__);
#define log_warn(...) log_with_level(LOG_WARNING, __VA_ARGS__);
#define log_error(...) log_with_level(LOG_ERROR, __VA_ARGS__);
