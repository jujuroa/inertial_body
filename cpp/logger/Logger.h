/*
 * Looger.h
 *
 *  Created on: Oct 31, 2025
 *      Author: youngh.kim
 */

#ifndef LOGGER_LOGGER_H_
#define LOGGER_LOGGER_H_

#include <iostream>
#include <cstdio>
#include <cstdarg>
#include <string>

namespace logger {

constexpr const char *const COLOR_RESET = 	"\x1b[0m";
constexpr const char *const COLOR_RED = 	"\x1b[31m";
constexpr const char *const COLOR_GREEN = 	"\x1b[32m";
constexpr const char *const COLOR_YELLOW = 	"\x1b[33m";
constexpr const char *const COLOR_BLUE = 	"\x1b[34m";
constexpr const char *const COLOR_MAGENTA = "\x1b[35m";
constexpr const char *const COLOR_CYAN = 	"\x1b[36m";

typedef enum {
    DEBUG,
    INFO,
    WARN,
    ERROR,
    FATAL
} Level;

static inline void printLog(Level level, const char *file, int line, const char *format, ...) {
    const char *level_str;
    const char *color;
    // 1. Set log level and print color
    switch (level) {
        case DEBUG:
            level_str = "DEBUG";
            color = COLOR_CYAN;
            break;
        case INFO:
            level_str = "INFO ";
            color = COLOR_GREEN;
            break;
        case WARN:
            level_str = "WARN ";
            color = COLOR_YELLOW;
            break;
        case ERROR:
            level_str = "ERROR";
            color = COLOR_RED;
            break;
        case FATAL:
            level_str = "FATAL";
            color = COLOR_MAGENTA;
            break;
        default:
            level_str = "UNKNOWN";
            color = COLOR_RESET;
            break;
    }

    fprintf(stderr, "%s[%s]%s [%s:%d] ", color, level_str, COLOR_RESET, file, line);

    va_list args;
    va_start(args, format);
    vfprintf(stderr, format, args);
    va_end(args);

    fprintf(stderr, "\n");
}

}  // namespace log


#define LOGD(format, ...) logger::printLog(logger::Level::DEBUG, __FUNCTION__, __LINE__, format, ##__VA_ARGS__)
#define LOGI(format, ...) logger::printLog(logger::Level::INFO, __FUNCTION__, __LINE__, format, ##__VA_ARGS__)
#define LOGW(format, ...) logger::printLog(logger::Level::WARN, __FUNCTION__, __LINE__, format, ##__VA_ARGS__)
#define LOGE(format, ...) logger::printLog(logger::Level::ERROR, __FUNCTION__, __LINE__, format, ##__VA_ARGS__)
#define LOGF(format, ...) logger::printLog(logger::Level::FATAL, __FUNCTION__, __LINE__, format, ##__VA_ARGS__)


#endif /* LOGGER_LOGGER_H_ */
