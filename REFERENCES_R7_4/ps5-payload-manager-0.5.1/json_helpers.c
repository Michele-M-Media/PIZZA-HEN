#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <ctype.h>
#include <sys/stat.h>
#include "json_helpers.h"

int json_append(JsonListBuilder *jb, const char *fmt, ...) {
    va_list args;
    int written;

    if (jb->pos >= jb->size) {
        return -1;
    }

    va_start(args, fmt);
    written = vsnprintf(jb->buf + jb->pos, jb->size - jb->pos, fmt, args);
    va_end(args);

    if (written < 0) {
        return -1;
    }

    if ((size_t)written >= jb->size - jb->pos) {
        jb->pos = jb->size - 1;
        jb->buf[jb->pos] = '\0';
        return -1;
    }

    jb->pos += (size_t)written;
    return 0;
}

int json_extract_string(const char *obj_start, const char *obj_end,
                        const char *key, char *out, size_t out_size) {
    char key_pattern[96];
    const char *p;
    const char *colon;
    const char *q;
    size_t pos = 0;

    if (out_size == 0) {
        return -1;
    }
    out[0] = '\0';

    snprintf(key_pattern, sizeof(key_pattern), "\"%s\"", key);
    p = strstr(obj_start, key_pattern);
    if (!p || p >= obj_end) {
        return -1;
    }

    colon = strchr(p + strlen(key_pattern), ':');
    if (!colon || colon >= obj_end) {
        return -1;
    }

    q = colon + 1;
    while (q < obj_end && isspace((unsigned char)*q)) {
        q++;
    }
    if (q >= obj_end || *q != '"') {
        return -1;
    }
    q++;

    while (q < obj_end && *q != '"') {
        if (*q == '\\' && (q + 1) < obj_end) {
            q++;
        }
        if (pos + 1 < out_size) {
            out[pos++] = *q;
        }
        q++;
    }
    out[pos] = '\0';
    return 0;
}

int read_file_text(const char *path, char **out_buf, size_t *out_size) {
    FILE *f;
    long fsize;
    char *buf;
    size_t nread;

    *out_buf = NULL;
    *out_size = 0;

    f = fopen(path, "rb");
    if (!f) {
        return -1;
    }

    if (fseek(f, 0, SEEK_END) != 0) {
        fclose(f);
        return -1;
    }
    fsize = ftell(f);
    if (fsize < 0) {
        fclose(f);
        return -1;
    }
    if (fseek(f, 0, SEEK_SET) != 0) {
        fclose(f);
        return -1;
    }

    buf = (char *)malloc((size_t)fsize + 1);
    if (!buf) {
        fclose(f);
        return -1;
    }

    nread = fread(buf, 1, (size_t)fsize, f);
    fclose(f);
    buf[nread] = '\0';

    *out_buf = buf;
    *out_size = nread;
    return 0;
}

int write_file_text(const char *path, const char *data, size_t size) {
    FILE *f = fopen(path, "wb");
    if (!f) {
        return -1;
    }
    if (fwrite(data, 1, size, f) != size) {
        fclose(f);
        return -1;
    }
    fclose(f);
    return 0;
}

int mkdir_if_missing(const char *path) {
    struct stat st;
    if (stat(path, &st) == 0) {
        return S_ISDIR(st.st_mode) ? 0 : -1;
    }
    return mkdir(path, 0777);
}

int ensure_dir_recursive(const char *path) {
    char tmp[512];
    size_t len = strlen(path);
    if (len >= sizeof(tmp)) {
        return -1;
    }

    strncpy(tmp, path, sizeof(tmp));
    tmp[len] = '\0';

    for (size_t i = 1; i < len; i++) {
        if (tmp[i] == '/') {
            tmp[i] = '\0';
            if (strlen(tmp) > 0 && mkdir_if_missing(tmp) != 0) {
                return -1;
            }
            tmp[i] = '/';
        }
    }
    return mkdir_if_missing(tmp);
}
