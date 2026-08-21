/* Small adapter so the vendored elfldr.c (see elfldr.c/elfldr.h) can log
 * through cr_log instead of upstream's own stdout+klog macros. */
#pragma once

#include <errno.h>
#include <string.h>

#include "cr_log.h"
#include "pt.h"

#define LOG_PUTS(s) cr_log("warn", "elfldr", "%s", (s))
#define LOG_PERROR(s) cr_log("warn", "elfldr", "%s: %s", (s), strerror(errno))
#define LOG_PT_PERROR(pid, s) pt_perror((pid), (s))
