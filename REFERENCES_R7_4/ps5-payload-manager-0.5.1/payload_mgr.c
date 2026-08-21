/*
 * Payload Manager — Local payload storage management.
 *
 * Handles scanning, listing, importing, deleting, and USB transfer
 * of ELF/BIN payload files on the PS5.
 */

#include <ctype.h>
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>

#include "payload_mgr.h"
#include "json_helpers.h"
#include "sha256.h"
#include "repository.h"
#include "config.h"
#include "pldmgr.h"

/* ── Extension / path checks ──────────────────────────────── */

static int is_supported_extension(const char *path) {
    const char *ext = strrchr(path, '.');
    if (!ext)
        return 0;
    return (strcasecmp(ext, ".elf") == 0 || strcasecmp(ext, ".bin") == 0);
}

static int is_allowed_usb_path(const char *path) {
    if (!path || path[0] == '\0')
        return 0;
    if (strstr(path, ".."))
        return 0;
    if (!is_supported_extension(path))
        return 0;
    if (strncmp(path, "/mnt/usb", 8) == 0 && path[8] >= '0' && path[8] <= '7' &&
        path[9] == '/')
        return 1;
    return 0;
}

/* ── File utilities ────────────────────────────────────────── */

static int copy_file(const char *src, const char *dst) {
    FILE *in = fopen(src, "rb");
    if (!in)
        return -1;
    FILE *out = fopen(dst, "wb");
    if (!out) {
        fclose(in);
        return -1;
    }
    char buf[8192];
    size_t n;
    while ((n = fread(buf, 1, sizeof(buf), in)) > 0) {
        if (fwrite(buf, 1, n, out) != n) {
            fclose(in);
            fclose(out);
            return -1;
        }
    }
    fclose(in);
    fclose(out);
    return 0;
}

/* Remove all files in a payload directory EXCEPT the new incoming file.
 * Also updates the autoload config if a file is being replaced. */
void payload_mgr_remove_old_files(const char *dir_path, const char *new_filename) {
    DIR *d = opendir(dir_path);
    if (!d) return;

    struct dirent *entry;
    while ((entry = readdir(d)) != NULL) {
        if (entry->d_name[0] == '.') continue;
        if (strcmp(entry->d_name, new_filename) == 0) continue;
        /* Skip .json metadata files for the incoming file */
        {
            size_t new_len = strlen(new_filename);
            size_t ent_len = strlen(entry->d_name);
            if (ent_len == new_len + 5 &&
                strncmp(entry->d_name, new_filename, new_len) == 0 &&
                strcmp(entry->d_name + new_len, ".json") == 0)
                continue;
        }

        char full_path[640];
        snprintf(full_path, sizeof(full_path), "%s/%s", dir_path, entry->d_name);

        /* If it's a supported payload, update autoload config */
        if (is_supported_extension(entry->d_name)) {
            pldmgr_autoload_update_config_entry(entry->d_name, new_filename);
        }

        remove(full_path);
    }
    closedir(d);
}

/* ── Recursive scan ────────────────────────────────────────── */

typedef struct {
    char path[512];
    char filename[256];
    int  is_storage;
    long mtime;
} PayloadEntry;

static void scan_payloads_recursive(const char *dir_path, int is_storage,
                                    PayloadEntry **out, int *count, int max, int max_depth) {
    if (max_depth < 0) return;

    DIR *d = opendir(dir_path);
    if (!d) return;

    struct dirent *entry;
    while (*count < max && (entry = readdir(d)) != NULL) {
        if (entry->d_name[0] == '.')
            continue;

        char full_path[512];
        snprintf(full_path, sizeof(full_path), "%s/%s", dir_path, entry->d_name);

        struct stat st;
        if (stat(full_path, &st) != 0)
            continue;

        if (S_ISDIR(st.st_mode)) {
            scan_payloads_recursive(full_path, is_storage, out, count, max, max_depth - 1);
            continue;
        }

        if (!is_supported_extension(entry->d_name))
            continue;

        PayloadEntry *tmp = realloc(*out, (*count + 1) * sizeof(PayloadEntry));
        if (!tmp) break;
        *out = tmp;

        strncpy((*out)[*count].path, full_path, sizeof((*out)[*count].path) - 1);
        (*out)[*count].path[sizeof((*out)[*count].path) - 1] = '\0';
        strncpy((*out)[*count].filename, entry->d_name, sizeof((*out)[*count].filename) - 1);
        (*out)[*count].filename[sizeof((*out)[*count].filename) - 1] = '\0';
        (*out)[*count].is_storage = is_storage;
        (*out)[*count].mtime = (long)st.st_mtime;
        (*count)++;
    }
    closedir(d);
}

/* ── Recursive resolve ─────────────────────────────────────── */

static int resolve_recursive(const char *dir_path, const char *filename,
                             char *out_path, size_t out_size) {
    DIR *d = opendir(dir_path);
    if (!d) return -1;

    struct dirent *entry;
    while ((entry = readdir(d)) != NULL) {
        if (entry->d_name[0] == '.')
            continue;

        char full[512];
        snprintf(full, sizeof(full), "%s/%s", dir_path, entry->d_name);

        struct stat st;
        if (stat(full, &st) != 0)
            continue;

        if (S_ISDIR(st.st_mode)) {
            if (resolve_recursive(full, filename, out_path, out_size) == 0) {
                closedir(d);
                return 0;
            }
            continue;
        }

        if (strcmp(entry->d_name, filename) == 0) {
            strncpy(out_path, full, out_size - 1);
            out_path[out_size - 1] = '\0';
            closedir(d);
            return 0;
        }
    }
    closedir(d);
    return -1;
}

/* ── Public API ────────────────────────────────────────────── */

size_t payload_mgr_list_json(char *json_buf, size_t buf_size) {
    PayloadEntry *payloads = NULL;
    int count = 0;
    int max = 256;
    int scan_usb = config_read_bool("SCAN_USB_PAYLOADS", 0);

    /* Scan pldmgr subdirs (this includes PAYLOADS_STORAGE_DIR under /data/pldmgr) */
    for (int i = 0; i < SCAN_DIRS_COUNT; i++) {
        scan_payloads_recursive(SCAN_DIRS[i], 0, &payloads, &count, max, 3);
    }

    /* Optionally scan USB root directories */
    if (scan_usb) {
        for (int usb = 0; usb < 8; usb++) {
            char usb_root[64];
            snprintf(usb_root, sizeof(usb_root), "/mnt/usb%d", usb);
            struct stat st;
            if (stat(usb_root, &st) == 0 && S_ISDIR(st.st_mode))
                scan_payloads_recursive(usb_root, 0, &payloads, &count, max, 0);
        }
    }

    /* Build JSON response */
    JsonListBuilder jb = { json_buf, buf_size, 0, 1 };
    json_append(&jb, "{\"payloads\":[");

    for (int i = 0; i < count; i++) {
        char path_escaped[1024];
        pldmgr_json_escape(payloads[i].path, path_escaped, sizeof(path_escaped));
        json_append(&jb, "%s\"%s\"", (i > 0) ? "," : "", path_escaped);
    }

    json_append(&jb, "],\"meta\":{");

    int meta_first = 1;
    for (int i = 0; i < count; i++) {
        /* Try to load sidecar .json metadata */
        char details_path[640];
        snprintf(details_path, sizeof(details_path), "%s.json", payloads[i].path);
        char *details_json = NULL;
        size_t details_size = 0;

        if (read_file_text(details_path, &details_json, &details_size) == 0 && details_json) {
            /* Extract fields from sidecar */
            char d_name[256] = "", d_desc[1024] = "", d_ver[64] = "", d_url[1024] = "";
            char d_src[1024] = "", d_src_direct[1024] = "", d_last_update[64] = "";
            char d_checksum[65] = "", d_downloaded[64] = "";
            char d_install_src[128] = "", d_install_detail[1024] = "";
            char d_source_name[256] = "";

            const char *end = details_json + details_size;
            json_extract_string(details_json, end, "name", d_name, sizeof(d_name));
            json_extract_string(details_json, end, "description", d_desc, sizeof(d_desc));
            json_extract_string(details_json, end, "version", d_ver, sizeof(d_ver));
            json_extract_string(details_json, end, "url", d_url, sizeof(d_url));
            json_extract_string(details_json, end, "source", d_src, sizeof(d_src));
            json_extract_string(details_json, end, "source_direct", d_src_direct, sizeof(d_src_direct));
            json_extract_string(details_json, end, "last_update", d_last_update, sizeof(d_last_update));
            json_extract_string(details_json, end, "checksum", d_checksum, sizeof(d_checksum));
            json_extract_string(details_json, end, "downloaded_at", d_downloaded, sizeof(d_downloaded));
            json_extract_string(details_json, end, "install_source", d_install_src, sizeof(d_install_src));
            json_extract_string(details_json, end, "install_source_detail", d_install_detail, sizeof(d_install_detail));
            json_extract_string(details_json, end, "source_name", d_source_name, sizeof(d_source_name));

            char filename_escaped[512], ne[512], de[2048], ve[128], ue[2048], se[2048], sde[2048];
            char lue[128], ce[128], dae[128], ise[256], ide[2048], sne[512];
            pldmgr_json_escape(payloads[i].filename, filename_escaped, sizeof(filename_escaped));
            pldmgr_json_escape(d_name, ne, sizeof(ne));
            pldmgr_json_escape(d_desc, de, sizeof(de));
            pldmgr_json_escape(d_ver, ve, sizeof(ve));
            pldmgr_json_escape(d_url, ue, sizeof(ue));
            pldmgr_json_escape(d_src, se, sizeof(se));
            pldmgr_json_escape(d_src_direct, sde, sizeof(sde));
            pldmgr_json_escape(d_last_update, lue, sizeof(lue));
            pldmgr_json_escape(d_checksum, ce, sizeof(ce));
            pldmgr_json_escape(d_downloaded, dae, sizeof(dae));
            pldmgr_json_escape(d_install_src, ise, sizeof(ise));
            pldmgr_json_escape(d_install_detail, ide, sizeof(ide));
            pldmgr_json_escape(d_source_name, sne, sizeof(sne));

            json_append(&jb, "%s\"%s\":{"
                        "\"display_name\":\"%s\",\"description\":\"%s\",\"version\":\"%s\","
                        "\"url\":\"%s\",\"source\":\"%s\",\"source_direct\":\"%s\","
                        "\"last_update\":\"%s\",\"checksum\":\"%s\",\"downloaded_at\":\"%s\","
                        "\"install_source\":\"%s\",\"install_source_detail\":\"%s\","
                        "\"source_name\":\"%s\"}",
                        meta_first ? "" : ",",
                        filename_escaped,
                        ne, de, ve, ue, se, sde, lue, ce, dae, ise, ide, sne);
            
            meta_first = 0;
            free(details_json);
        }
    }

    json_append(&jb, "}}");

    if (payloads)
        free(payloads);

    return jb.pos;
}

int payload_mgr_resolve_path(const char *filename, char *out_path, size_t out_size) {
    for (int i = 0; i < SCAN_DIRS_COUNT; i++) {
        if (resolve_recursive(SCAN_DIRS[i], filename, out_path, out_size) == 0)
            return 0;
    }
    return -1;
}

int payload_mgr_delete_payload_file(const char *filename) {
    char resolved[512];
    if (!filename || strstr(filename, "/") || strstr(filename, ".."))
        return -1;

    if (payload_mgr_resolve_path(filename, resolved, sizeof(resolved)) != 0)
        return -1;

    /* Also remove .json sidecar */
    char meta_path[640];
    snprintf(meta_path, sizeof(meta_path), "%s.json", resolved);
    remove(meta_path);

    /* Update autoload config */
    pldmgr_autoload_update_config_entry(filename, NULL);

    return remove(resolved);
}

int payload_mgr_import_to_storage(const char *filename, const char *temp_path,
                                  const char *install_source, const char *install_source_detail,
                                  char *msg_buf, size_t msg_buf_size) {
    if (!filename || strstr(filename, "/") || strstr(filename, "..")) {
        snprintf(msg_buf, msg_buf_size, "Invalid filename");
        return -1;
    }

    char folder_name[128];
    pldmgr_utils_get_payload_folder_name(filename, folder_name, sizeof(folder_name));

    char payload_dir[512];
    snprintf(payload_dir, sizeof(payload_dir), "%s/%s", PAYLOADS_STORAGE_DIR, folder_name);
    if (ensure_dir_recursive(payload_dir) != 0) {
        snprintf(msg_buf, msg_buf_size, "Failed to create directory");
        return -1;
    }

    char final_path[640];
    snprintf(final_path, sizeof(final_path), "%s/%s", payload_dir, filename);

    /* Remove old files in the payload directory */
    payload_mgr_remove_old_files(payload_dir, filename);

    if (rename(temp_path, final_path) != 0) {
        snprintf(msg_buf, msg_buf_size, "Failed to move file");
        return -1;
    }

    /* Write metadata sidecar */
    char details_path[700];
    snprintf(details_path, sizeof(details_path), "%s/%s.json", payload_dir, filename);
    write_simple_payload_details_json(filename, details_path, install_source, install_source_detail);

    pldmgr_log("[PLDMGR] Imported payload: %s -> %s\n", filename, final_path);
    snprintf(msg_buf, msg_buf_size, "Imported %s", filename);
    return 0;
}

int payload_mgr_check_existing(const char *filename, char *out_json, size_t out_size) {
    char folder_name[128];
    char folder_path[512];
    char file_path[640];
    struct stat st;

    pldmgr_utils_get_payload_folder_name(filename, folder_name, sizeof(folder_name));
    snprintf(folder_path, sizeof(folder_path), "%s/%s", PAYLOADS_STORAGE_DIR, folder_name);
    snprintf(file_path, sizeof(file_path), "%s/%s", folder_path, filename);

    int folder_exists = (stat(folder_path, &st) == 0 && S_ISDIR(st.st_mode));
    int file_exists = (stat(file_path, &st) == 0 && S_ISREG(st.st_mode));

    snprintf(out_json, out_size, "{\"status\":\"ok\",\"folder_exists\":%s,\"file_exists\":%s,\"folder_name\":\"%s\"}",
             folder_exists ? "true" : "false", file_exists ? "true" : "false", folder_name);
    return 0;
}

int payload_mgr_write_metadata(const char *payload_path, const char *install_source,
                               const char *install_source_detail) {
    char details_path[700];
    const char *filename = strrchr(payload_path, '/');
    filename = filename ? filename + 1 : payload_path;
    snprintf(details_path, sizeof(details_path), "%s.json", payload_path);
    return write_simple_payload_details_json(filename, details_path, install_source, install_source_detail);
}

/* ── USB Check / Move ──────────────────────────────────────── */

int payload_mgr_usb_check(const char *usb_path, char *out_json, size_t out_size) {
    if (!is_allowed_usb_path(usb_path)) {
        snprintf(out_json, out_size, "{\"error\":\"Invalid USB path\"}");
        return -1;
    }

    struct stat st;
    if (stat(usb_path, &st) != 0) {
        snprintf(out_json, out_size, "{\"error\":\"File not found\"}");
        return -1;
    }

    const char *filename = strrchr(usb_path, '/');
    filename = filename ? filename + 1 : usb_path;

    char existing_path[512];
    int exists = (payload_mgr_resolve_path(filename, existing_path, sizeof(existing_path)) == 0);

    char name_e[512], path_e[1024];
    pldmgr_json_escape(filename, name_e, sizeof(name_e));
    pldmgr_json_escape(usb_path, path_e, sizeof(path_e));

    snprintf(out_json, out_size,
             "{\"filename\":\"%s\",\"path\":\"%s\",\"size\":%lld,\"exists\":%s}",
             name_e, path_e, (long long)st.st_size, exists ? "true" : "false");
    return 0;
}

int payload_mgr_usb_move(const char *usb_path, int overwrite, int keep_original, char *out_json,
                         size_t out_size) {
    if (!is_allowed_usb_path(usb_path)) {
        snprintf(out_json, out_size, "{\"ok\":false,\"message\":\"Invalid USB path\"}");
        return -1;
    }

    struct stat st;
    if (stat(usb_path, &st) != 0) {
        snprintf(out_json, out_size, "{\"ok\":false,\"message\":\"File not found\"}");
        return -1;
    }

    const char *filename = strrchr(usb_path, '/');
    filename = filename ? filename + 1 : usb_path;

    char folder_name[128];
    pldmgr_utils_get_payload_folder_name(filename, folder_name, sizeof(folder_name));

    char payload_dir[512];
    snprintf(payload_dir, sizeof(payload_dir), "%s/%s", PAYLOADS_STORAGE_DIR, folder_name);
    ensure_dir_recursive(payload_dir);

    char final_path[640];
    snprintf(final_path, sizeof(final_path), "%s/%s", payload_dir, filename);

    /* Check for existing file */
    if (!overwrite && access(final_path, F_OK) == 0) {
        snprintf(out_json, out_size, "{\"ok\":false,\"message\":\"File already exists\","
                 "\"exists\":true}");
        return -1;
    }

    /* Remove old files if overwriting */
    if (overwrite) {
        payload_mgr_remove_old_files(payload_dir, filename);
    }

    if (copy_file(usb_path, final_path) != 0) {
        snprintf(out_json, out_size, "{\"ok\":false,\"message\":\"Copy failed\"}");
        return -1;
    }

    /* Write metadata */
    char details_path[700];
    snprintf(details_path, sizeof(details_path), "%s/%s.json", payload_dir, filename);
    write_simple_payload_details_json(filename, details_path, "usb", usb_path);

    /* Remove the original file if not copying */
    if (!keep_original) {
        if (remove(usb_path) != 0) {
            pldmgr_log("[PLDMGR] Warning: Failed to remove original file from USB: %s\n", usb_path);
            snprintf(out_json, out_size, "{\"ok\":true,\"message\":\"Moved successfully\",\"warning\":\"Payload copied, but failed to delete original from USB.\"}");
        } else {
            pldmgr_log("[PLDMGR] USB payload moved: %s -> %s\n", usb_path, final_path);
            snprintf(out_json, out_size, "{\"ok\":true,\"message\":\"Moved successfully\"}");
        }
    } else {
        pldmgr_log("[PLDMGR] USB payload copied: %s -> %s\n", usb_path, final_path);
        snprintf(out_json, out_size, "{\"ok\":true,\"message\":\"Copied successfully\"}");
    }
    return 0;
}
