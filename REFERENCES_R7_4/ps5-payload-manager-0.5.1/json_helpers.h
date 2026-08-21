#ifndef JSON_HELPERS_H
#define JSON_HELPERS_H

#include <stddef.h>

/* Incremental JSON array/object builder */
typedef struct JsonListBuilder {
    char *buf;
    size_t size;
    size_t pos;
    int first;
} JsonListBuilder;

/* Append formatted text to the builder. Returns 0 on success, -1 on overflow. */
int json_append(JsonListBuilder *jb, const char *fmt, ...);

/* Extract a quoted string value for a given key from a JSON object bounded by
 * [obj_start, obj_end). Returns 0 on success, -1 if key not found. */
int json_extract_string(const char *obj_start, const char *obj_end,
                        const char *key, char *out, size_t out_size);

/* Read an entire file into a malloc'd buffer. Caller must free *out_buf.
 * Returns 0 on success, -1 on failure. */
int read_file_text(const char *path, char **out_buf, size_t *out_size);

/* Write data to a file atomically. Returns 0 on success, -1 on failure. */
int write_file_text(const char *path, const char *data, size_t size);

/* Create a directory if it doesn't exist. Returns 0 on success. */
int mkdir_if_missing(const char *path);

/* Recursively create all directories in path. Returns 0 on success. */
int ensure_dir_recursive(const char *path);

#endif
