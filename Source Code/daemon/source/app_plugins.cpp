/*
 * PIZZA HEN - etaHEN 2.6B application-plugin delta compatibility layer.
 * FIX45: lifecycle/status model inspired by the source-available PS5 Payload
 * Manager: configuration state is kept separate from runtime state, autoload
 * is session-aware, failures can retry, and status is published atomically.
 *
 * This intentionally extends the existing PIZZA HEN daemon instead of
 * replacing it with the etaHEN 2.6B binary.  The public configuration model
 * mirrors the strings embedded in etaHEN 2.6B: [DEFAULT], per-title sections,
 * arbitrary plugin paths and the ?autoload suffix.
 *
 * Runtime loading reuses the already-integrated NineS ELF injector.  No new
 * firmware offsets or SDK-version dependencies are introduced here.
 */

#include <algorithm>
#include <cctype>
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <fcntl.h>
#include <string>
#include <sys/stat.h>
#include <unistd.h>
#include <vector>
#include <utility>

extern "C" {
int sceSystemServiceGetAppIdOfRunningBigApp(void);
int sceSystemServiceGetAppTitleId(int app_id, char *title_id);
bool Inject_Toolbox(int pid, uint8_t *elf);
}

extern int get_game_pid();
extern void etaHEN_log(const char *fmt, ...);

namespace {
constexpr const char *kAppsDir = "/data/PIZZA_HEN/plugins/apps";
constexpr const char *kConfigPath = "/data/PIZZA_HEN/plugins/apps/plugins.ini";
constexpr const char *kRuntimeDir = "/data/PIZZA_HEN/runtime";
constexpr const char *kStatusPath = "/data/PIZZA_HEN/runtime/app_plugins_status.txt";

struct AppPluginEntry {
    std::string section;
    std::string path;
    bool autoload = false;
};

static std::string g_last_published_status;

static std::string trim_copy(const std::string &in) {
    size_t first = 0;
    while (first < in.size() && std::isspace(static_cast<unsigned char>(in[first])))
        ++first;
    size_t last = in.size();
    while (last > first && std::isspace(static_cast<unsigned char>(in[last - 1])))
        --last;
    return in.substr(first, last - first);
}

static bool ends_with(const std::string &value, const char *suffix) {
    const size_t n = std::strlen(suffix);
    return value.size() >= n && value.compare(value.size() - n, n, suffix) == 0;
}

static bool ensure_dir(const char *path) {
    struct stat st{};
    if (stat(path, &st) == 0)
        return S_ISDIR(st.st_mode);
    return mkdir(path, 0777) == 0;
}

static bool write_all(int fd, const char *data, size_t size) {
    size_t done = 0;
    while (done < size) {
        const ssize_t wrote = write(fd, data + done, size - done);
        if (wrote <= 0)
            return false;
        done += static_cast<size_t>(wrote);
    }
    return true;
}

static bool atomic_write_text(const char *path, const std::string &text) {
    const std::string tmp = std::string(path) + ".tmp";
    int fd = open(tmp.c_str(), O_WRONLY | O_CREAT | O_TRUNC, 0666);
    if (fd < 0)
        return false;

    const bool ok = write_all(fd, text.data(), text.size());
    if (ok)
        (void)fsync(fd);
    close(fd);

    if (!ok || rename(tmp.c_str(), path) != 0) {
        unlink(tmp.c_str());
        return false;
    }
    return true;
}

static std::string status_safe(std::string value) {
    for (char &c : value) {
        if (c == '\n' || c == '\r' || c == '=')
            c = ' ';
    }
    return value;
}

static void publish_status(const char *state,
                           const std::string &tid,
                           int pid,
                           int configured,
                           int armed,
                           int loaded,
                           const std::string &current,
                           const std::string &last_result) {
    (void)ensure_dir("/data/PIZZA_HEN");
    (void)ensure_dir(kRuntimeDir);

    std::string text;
    text.reserve(512);
    text += "version=1\n";
    text += "state=" + status_safe(state ? state : "unknown") + "\n";
    text += "title_id=" + status_safe(tid.empty() ? "-" : tid) + "\n";
    text += "pid=" + std::to_string(pid) + "\n";
    text += "configured=" + std::to_string(configured) + "\n";
    text += "armed=" + std::to_string(armed) + "\n";
    text += "loaded=" + std::to_string(loaded) + "\n";
    text += "current=" + status_safe(current.empty() ? "-" : current) + "\n";
    text += "last_result=" + status_safe(last_result.empty() ? "-" : last_result) + "\n";

    // Avoid writing the same status every polling cycle.
    if (text == g_last_published_status)
        return;
    if (atomic_write_text(kStatusPath, text))
        g_last_published_status = text;
}

static void ensure_config_template() {
    (void)ensure_dir("/data/PIZZA_HEN/plugins");
    (void)ensure_dir(kAppsDir);

    struct stat st{};
    if (stat(kConfigPath, &st) == 0)
        return;

    static const char kTemplate[] =
        "; PIZZA HEN Application Plugins - etaHEN 2.6B compatible format\n"
        ";\n"
        "; [DEFAULT] entries are considered for every application.\n"
        "; Plugin paths are not limited to the PIZZA HEN folder.\n"
        "; Add ?autoload to a path to arm it for the matching application.\n"
        "; Removing ?autoload disarms future automatic loading.\n"
        "; Runtime loaded state is separate from the saved autoload setting.\n"
        "; A plugin already loaded remains resident until the application closes.\n"
        ";\n"
        "; [DEFAULT]\n"
        "; /data/PIZZA_HEN/plugins/apps/plugin.sprx?autoload\n"
        ";\n"
        "; [CUSA00001]\n"
        "; /data/PIZZA_HEN/plugins/apps/plugin.sprx\n"
        ";\n"
        "; [PPSA00001]\n"
        "; /data/plugin.sprx?autoload\n"
        ";\n"
        "; The same plugin path may appear under multiple title IDs.\n"
        "; /mnt/usb0/plugin.sprx\n";

    int fd = open(kConfigPath, O_WRONLY | O_CREAT | O_EXCL, 0666);
    if (fd < 0)
        return;
    (void)write_all(fd, kTemplate, sizeof(kTemplate) - 1);
    close(fd);
    etaHEN_log("[app-plugin] created %s", kConfigPath);
}

static bool read_text_file(const char *path, std::string &out) {
    int fd = open(path, O_RDONLY);
    if (fd < 0)
        return false;
    struct stat st{};
    if (fstat(fd, &st) != 0 || st.st_size < 0 || st.st_size > (1024 * 1024)) {
        close(fd);
        return false;
    }
    out.assign(static_cast<size_t>(st.st_size), '\0');
    size_t done = 0;
    while (done < out.size()) {
        const ssize_t got = read(fd, &out[done], out.size() - done);
        if (got <= 0) {
            close(fd);
            return false;
        }
        done += static_cast<size_t>(got);
    }
    close(fd);
    return true;
}

static std::vector<AppPluginEntry> parse_config() {
    std::vector<AppPluginEntry> entries;
    std::string text;
    if (!read_text_file(kConfigPath, text))
        return entries;

    std::string section = "DEFAULT";
    size_t pos = 0;
    while (pos <= text.size()) {
        const size_t end = text.find('\n', pos);
        std::string line = text.substr(pos, end == std::string::npos ? std::string::npos : end - pos);
        if (!line.empty() && line.back() == '\r')
            line.pop_back();
        line = trim_copy(line);

        if (!line.empty() && line[0] != ';' && line[0] != '#') {
            if (line.size() >= 3 && line.front() == '[' && line.back() == ']') {
                section = trim_copy(line.substr(1, line.size() - 2));
            } else {
                AppPluginEntry entry;
                entry.section = section.empty() ? "DEFAULT" : section;
                entry.autoload = ends_with(line, "?autoload");
                entry.path = entry.autoload ? line.substr(0, line.size() - 9) : line;
                entry.path = trim_copy(entry.path);
                if (!entry.path.empty())
                    entries.push_back(std::move(entry));
            }
        }

        if (end == std::string::npos)
            break;
        pos = end + 1;
    }
    return entries;
}

static bool read_plugin_elf(const std::string &path, std::vector<uint8_t> &buf) {
    int fd = open(path.c_str(), O_RDONLY);
    if (fd < 0) {
        etaHEN_log("[app-plugin] cannot open %s", path.c_str());
        return false;
    }

    struct stat st{};
    if (fstat(fd, &st) != 0 || st.st_size < 4 || st.st_size > (64 * 1024 * 1024)) {
        close(fd);
        etaHEN_log("[app-plugin] invalid size for %s", path.c_str());
        return false;
    }

    buf.resize(static_cast<size_t>(st.st_size));
    size_t done = 0;
    while (done < buf.size()) {
        const ssize_t got = read(fd, buf.data() + done, buf.size() - done);
        if (got <= 0) {
            close(fd);
            return false;
        }
        done += static_cast<size_t>(got);
    }
    close(fd);

    static const uint8_t kElfMagic[4] = {0x7f, 'E', 'L', 'F'};
    if (std::memcmp(buf.data(), kElfMagic, sizeof(kElfMagic)) != 0) {
        etaHEN_log("[app-plugin] %s is not an ELF/SPRX image", path.c_str());
        return false;
    }
    return true;
}

static bool load_into_running_app(const std::string &path, const std::string &tid, int pid) {
    std::vector<uint8_t> elf;
    if (!read_plugin_elf(path, elf))
        return false;

    etaHEN_log("[app-plugin] loading %s for %s (PID %d)", path.c_str(), tid.c_str(), pid);
    if (!Inject_Toolbox(pid, elf.data())) {
        etaHEN_log("[app-plugin] injection failed: %s", path.c_str());
        return false;
    }
    etaHEN_log("[app-plugin] loaded: %s", path.c_str());
    return true;
}

static bool section_matches(const std::string &section, const std::string &tid) {
    return section == "DEFAULT" || section == tid;
}
} // namespace

void *app_plugin_monitor_thread(void *) {
    ensure_config_template();
    publish_status("idle", "", -1, 0, 0, 0, "", "waiting for application");

    int last_pid = -1;
    std::string last_tid;
    std::vector<std::string> loaded_paths;

    for (;;) {
        const int appid = sceSystemServiceGetAppIdOfRunningBigApp();
        char tid_buf[32] = {};
        if (appid < 0 || sceSystemServiceGetAppTitleId(appid, tid_buf) != 0 || tid_buf[0] == '\0') {
            if (last_pid != -1) {
                etaHEN_log("[app-plugin] application closed; clearing session state");
                last_pid = -1;
                last_tid.clear();
                loaded_paths.clear();
            }
            publish_status("idle", "", -1, 0, 0, 0, "", "waiting for application");
            sleep(2);
            continue;
        }

        const int pid = get_game_pid();
        if (pid <= 0) {
            publish_status("waiting_pid", tid_buf, pid, 0, 0, 0, "", "application detected; waiting for PID");
            sleep(2);
            continue;
        }

        const std::string tid(tid_buf);
        if (pid != last_pid || tid != last_tid) {
            etaHEN_log("[app-plugin] PID change detected (TID: %s | PID: %d)", tid.c_str(), pid);
            last_pid = pid;
            last_tid = tid;
            loaded_paths.clear();
        }

        const auto entries = parse_config();
        int configured_count = 0;
        int armed_count = 0;
        for (const auto &entry : entries) {
            if (!section_matches(entry.section, tid))
                continue;
            ++configured_count;
            if (entry.autoload)
                ++armed_count;
        }

        std::string last_plugin;
        std::string last_result = "monitoring";
        bool had_error = false;

        for (const auto &entry : entries) {
            if (!entry.autoload || !section_matches(entry.section, tid))
                continue;
            if (std::find(loaded_paths.begin(), loaded_paths.end(), entry.path) != loaded_paths.end())
                continue;

            last_plugin = entry.path;
            publish_status("loading", tid, pid, configured_count, armed_count,
                           static_cast<int>(loaded_paths.size()), entry.path, "loading");

            // Record only successful loads so a transient file/read failure can retry.
            if (load_into_running_app(entry.path, tid, pid)) {
                loaded_paths.push_back(entry.path);
                last_result = "loaded";
            } else {
                had_error = true;
                last_result = "load failed; will retry while app remains active";
            }
        }

        const char *state = had_error ? "error" :
                            (!loaded_paths.empty() ? "active" :
                            (armed_count > 0 ? "armed" : "monitoring"));
        publish_status(state, tid, pid, configured_count, armed_count,
                       static_cast<int>(loaded_paths.size()), last_plugin, last_result);

        sleep(2);
    }
    return nullptr;
}
