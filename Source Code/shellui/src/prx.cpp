
/* Copyright (C) 2025 etaHEN / LightningMods

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 3, or (at your option) any
later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; see the file COPYING. If not, see
<http://www.gnu.org/licenses/>.  */

#include "Detour.h"
#include "HookedFuncs.hpp"
#include "debug_services_route.hpp"
#include "hook_lifecycle.hpp"
#include "defs.h"
#include "external_symbols.hpp"
#include "ipc.hpp"
#include "proc.h"
#include "ps5/kernel.h"
#include "ucred.h"
#include <cstdint>
#include <iostream>
#include "webserver.hpp"

#include <unistd.h>
#include <util.hpp>

// R7.5.3.1: local forward declaration; frozen HookedFuncs.hpp remains byte-exact.
void PizzahenServiceWebControl();

std::string dec_xml_str;
std::string dec_list_xml_str;
std::string UI3_dec;
std::string legacy_dec;
std::string appsystem_dll;
std::string uilib;
std::string Sysinfo;
std::string display_info;
std::string uilib_dll;

std::string plugin_xml;
std::string remote_play_xml;
std::string debug_settings_xml;
std::string cheats_xml;

MonoImage* pui_img = nullptr;
MonoImage* AppSystem_img = nullptr;
MonoObject* Game = nullptr;
MonoImage * react_common_img = nullptr;

bool hooked = false;
bool g_pizzahen_shell_service_mode = false;
bool g_pizzahen_overlay_apply_requested = false;
static int g_pizzahen_service_bigapp_id = -2;
bool has_hv_bypass = false;
bool is_testkit = false;

extern "C" long ptr_syscall = 0;

void __syscall() {
  asm(".intel_syntax noprefix\n"
      "  mov rax, rdi\n"
      "  mov rdi, rsi\n"
      "  mov rsi, rdx\n"
      "  mov rdx, rcx\n"
      "  mov r10, r8\n"
      "  mov r8,  r9\n"
      "  mov r9,  qword ptr [rsp + 8]\n"
      "  call qword ptr [rip + ptr_syscall]\n"
      "  ret\n");
}

void (*OnRender_orig)(MonoObject* instance);
MonoObject* rootWidget = nullptr;
MonoObject* font = nullptr;

void (*Orig_ReloadApp)(MonoString *str) = nullptr;

void ReloadApp(MonoString *str){
     std::string tid = mono_string_to_utf8(str);
     shellui_log("Reloading %s scenes", tid.c_str());
     notify("Reloading %s scenes", tid.c_str());
     Orig_ReloadApp(str);
}

#define PLAYGOSCENARIOID_SIZE 3
#define CONTENTID_SIZE 0x30
#define LANGUAGE_SIZE 8

typedef char playgo_scenario_id_t[PLAYGOSCENARIOID_SIZE];
typedef char language_t[LANGUAGE_SIZE];
typedef char content_id_t[CONTENTID_SIZE];

typedef struct
{
    content_id_t content_id;
    int content_type;
    int content_platform;
} SceAppInstallPkgInfo;

typedef struct
{
    const char* uri;
    const char* ex_uri;
    const char* playgo_scenario_id;
    const char* content_id;
    const char* content_name;
    const char* icon_url;
} MetaInfo;

#define NUM_LANGUAGES 30
#define NUM_IDS 64

typedef struct {
    language_t languages[NUM_LANGUAGES];
    playgo_scenario_id_t playgo_scenario_ids[NUM_IDS];
    content_id_t content_ids[NUM_IDS];
    long unknown[810];
} PlayGoInfo;


//int _AppInstUtilInstallByPackage(string uri, string ex_uri, string playgo_scenario_id, string content_id, string content_name, string icon_url, uint slot, bool is_playgo_enabled, ref AppInstUtilWrapper.SceAppInstallPkgInfo pkg_info, string[] languages, string[] playgo_scenario_ids, string[] content_ids);

int (*Orig_AppInstUtilInstallByPackage)(MonoString* uri, MonoString* ex_uri, MonoString* playgo_scenario_id, MonoString* content_id, MonoString* content_name, MonoString* icon_url, uint32_t slot, bool is_playgo_enabled, MonoObject* pkg_info, MonoArray* languages, MonoArray* playgo_scenario_ids, MonoArray* content_ids) = nullptr;

int AppInstUtilInstallByPackage_Hook(MonoString* uri, MonoString* ex_uri, MonoString* playgo_scenario_id, MonoString* content_id, MonoString* content_name, MonoString* icon_url, uint32_t slot, bool is_playgo_enabled, MonoObject* pkg_info, MonoArray* languages, MonoArray* playgo_scenario_ids, MonoArray* content_ids) {
        std::string s_uri = mono_string_to_utf8(uri);
    std::string s_ex_uri = mono_string_to_utf8(ex_uri);
    std::string s_playgo_scenario_id = mono_string_to_utf8(playgo_scenario_id);
    std::string s_content_id = mono_string_to_utf8(content_id);
    std::string s_content_name = mono_string_to_utf8(content_name);
    std::string s_icon_url = mono_string_to_utf8(icon_url);
    shellui_log("AppInstUtilInstallByPackage_Hook called with:\n uri: %s\n ex_uri: %s\n playgo_scenario_id: %s\n content_id: %s\n content_name: %s\n icon_url: %s\n slot: %u\n is_playgo_enabled: %d", 
        s_uri.c_str(), s_ex_uri.c_str(), s_playgo_scenario_id.c_str(), s_content_id.c_str(), s_content_name.c_str(), s_icon_url.c_str(), slot, is_playgo_enabled);
    notify("Installing package from:\n%s", s_uri.c_str());
    int ret = Orig_AppInstUtilInstallByPackage(uri, ex_uri, playgo_scenario_id, content_id, content_name, icon_url, slot, is_playgo_enabled, pkg_info, languages, playgo_scenario_ids, content_ids);
    shellui_log("AppInstUtilInstallByPackage_Hook returned: %d", ret);
    notify("Installation finished with code: %d", ret);
	return ret;
}

struct OrbisKernelTimespec {
    int64_t tv_sec;
    int64_t tv_nsec;
};

struct Proc_Stats
{
    int32_t lo_data;								//0x00
    uint32_t td_tid;						//0x04
    OrbisKernelTimespec user_cpu_usage_time;	//0x08
    OrbisKernelTimespec system_cpu_usage_time;  //0x18
}; //0x28

extern "C" {
    int sceKernelGetSocSensorTemperature(int sensorId, int* soctime);
    int get_page_table_stats(int vm, int type, int* total, int* free);
    int sceKernelGetCpuUsage(struct Proc_Stats* out, int32_t* size);
    int sceKernelGetThreadName(uint32_t id, char* out);
	int sceKernelGetCpuTemperature(int* cputemp);
    int sceKernelClockGettime(int clockId, OrbisKernelTimespec* tp);
}

struct Memory
{
    int Used;
    int Free;
    int Total;
    float Percentage;
};

struct thread_usages
{
    OrbisKernelTimespec current_time;	//0x00
    int Thread_Count;					//0x10
    char padding0[0x4];					//0x14
    Proc_Stats Threads[3072];			//0x18
};

int Thread_Count = 0;
float Usage[8] = { 0 };
float Average_Usage;
Memory RAM;
Memory VRAM;

Proc_Stats Stat_Data[3072];
thread_usages gThread_Data[2];


extern "C" int sceLncUtilKillAppWithReason(int appId, int reason);
void pause_resume_kstuff(KstuffPauseStatus opt, bool notify_user);

int KillAppWithReason_Hook(int appId, int reason)
{
   // shellui_log("KillAppWithReason_Hook called with appId: %d, reason: %d", appId, reason);
    //notify("Killing app %d", appId);
    if(global_conf.enable_kstuff_on_close)
        pause_resume_kstuff(NOT_PAUSED, true);

    int ret = sceLncUtilKillAppWithReason(appId, reason);
    //shellui_log("KillAppWithReason_Hook returned: %d", ret);
    return ret;
}

void Get_Page_Table_Stats(int vm, int type, int* Used, int* Free, int* Total)
{
    int _Total = 0, _Free = 0;

    if (get_page_table_stats(vm, type, &_Total, &_Free) == -1) {
        shellui_log("get_page_table_stats() Failed.\n");
        return;
    }

    if (Used)
        *Used = (_Total - _Free);

    if (Free)
        *Free = _Free;

    if (Total)
        *Total = _Total;
}

void calc_usage(unsigned int idle_tid[8], thread_usages* cur, thread_usages* prev, float usage_out[8])
{
    if (cur->Thread_Count <= 0 || prev->Thread_Count <= 0) //Make sure our banks have threads
        return;

    //Calculate the Current time difference from the last bank to the current bank.
    float Current_Time_Total = ((prev->current_time.tv_sec + (prev->current_time.tv_nsec / 1000000000.0f)) - (cur->current_time.tv_sec + (cur->current_time.tv_nsec / 1000000000.0f)));

    //Here this could use to be improved but essetially what its doing is finding the thread information for the idle threads using their thread Index stored from before.
    struct Data_s
    {
        Proc_Stats* Cur;
        Proc_Stats* Prev;
    }Data[8];

    for (int i = 0; i < cur->Thread_Count; i++)
    {
        for (int j = 0; j < 8; j++)
        {
            if (idle_tid[j] == cur->Threads[i].td_tid)
                Data[j].Cur = &cur->Threads[i];
        }
    }

    for (int i = 0; i < prev->Thread_Count; i++)
    {
        for (int j = 0; j < 8; j++)
        {
            if (idle_tid[j] == prev->Threads[i].td_tid)
                Data[j].Prev = &prev->Threads[i];
        }
    }

    //Here we loop through each core to calculate the total usage time as its split into user/sustem
    for (int i = 0; i < 8; i++)
    {
        float Prev_Usage_Time = (Data[i].Prev->system_cpu_usage_time.tv_sec + (Data[i].Prev->system_cpu_usage_time.tv_nsec / 1000000.0f));
        Prev_Usage_Time += (Data[i].Prev->user_cpu_usage_time.tv_sec + (Data[i].Prev->user_cpu_usage_time.tv_nsec / 1000000.0f));

        float Cur_Usage_Time = (Data[i].Cur->system_cpu_usage_time.tv_sec + (Data[i].Cur->system_cpu_usage_time.tv_nsec / 1000000.0f));
        Cur_Usage_Time += (Data[i].Cur->user_cpu_usage_time.tv_sec + (Data[i].Cur->user_cpu_usage_time.tv_nsec / 1000000.0f));

        //We calculate the usage using usage time difference between the two samples divided by the current time difference.
        float Idle_Usage = ((Prev_Usage_Time - Cur_Usage_Time) / Current_Time_Total);

        if (Idle_Usage > 1.0f)
            Idle_Usage = 1.0f;

        if (Idle_Usage < 0.0f)
            Idle_Usage = 0.0f;

        //Get inverse of idle percentage and express in percent.
        usage_out[i] = (1.0f - Idle_Usage) * 100.0f;
    }
}
extern bool app_launched;


class AtomicString {
    mutable std::mutex mtx;
    std::string value;

public:
    void store(const std::string& str) {
        std::lock_guard<std::mutex> lock(mtx);
        value = str;
    }

    std::string load() const {
        std::lock_guard<std::mutex> lock(mtx);
        return value;
    }
};

void* search_bytes(const void* haystack, size_t haystack_len,
    const void* needle, size_t needle_len){

    if (needle_len == 0 || needle_len > haystack_len) {
        return NULL;

    }

    const unsigned char* h = (const unsigned char*)haystack;
    const unsigned char* n = (const unsigned char*)needle;


    for (size_t i = 0; i <= haystack_len - needle_len; i++) {
        if (memcmp(&h[i], n, needle_len) == 0) {
            return (void*)&h[i];

        }
    }

    return NULL;

}
void ShellHexDump(const void* data, size_t size) {
    const unsigned char* byteData = static_cast<const unsigned char*>(data);
    char line[256];
    
    for (size_t i = 0; i < size; i += 16) {
        int pos = 0;
        
        // Offset
        pos += snprintf(line + pos, sizeof(line) - pos, "%08zx  ", i);
        
        // Hex bytes
        for (size_t j = 0; j < 16; ++j) {
            if (i + j < size) {
                pos += snprintf(line + pos, sizeof(line) - pos, "%02x ", 
                                byteData[i + j]);
            } else {
                pos += snprintf(line + pos, sizeof(line) - pos, "   ");
            }
        }
        
        pos += snprintf(line + pos, sizeof(line) - pos, " ");
        
        // ASCII representation
        for (size_t j = 0; j < 16; ++j) {
            if (i + j < size) {
                unsigned char c = byteData[i + j];
                pos += snprintf(line + pos, sizeof(line) - pos, "%c", 
                                isprint(c) ? c : '.');
            }
        }
        
        shellui_log(line);
    }
}
AtomicString fps_string;
ssize_t(*read_orig)(int fd, void *buf, size_t count) = nullptr;
ssize_t read_hook(int fd, void* buf, size_t count) {
    ssize_t ret = read_orig(fd, buf, count);
   // shellui_log("read_hook called: fd=%d, count=%zu, ret=%zd", fd, count, ret);
    if (count == 65536) {
        void* found = search_bytes(buf, 100, "FPS", 3);
        if (found) {
            const char* fps_ptr = (const char*)found;

            // Skip "FPS" and any separators (: = space etc)
            fps_ptr += 3; // Skip "FPS"
            while (*fps_ptr && !isdigit(*fps_ptr)) {
                fps_ptr++;
            }

            // Extract the number
            std::string fps_value;
            while (*fps_ptr && (isdigit(*fps_ptr) || *fps_ptr == '.')) {
                fps_value += *fps_ptr;
                fps_ptr++;
            }

            if (!fps_value.empty()) {
                fps_string.store(fps_value);
              //  shellui_log("Captured FPS: %s", fps_value.c_str());
            }
            return -1;
        }
    }
    return ret;
}

int get_ip_address(char* ip_address);

static bool pizzahen_resolve_game_scene() {
    if (Game) return true;
    if (!AppSystem_img || !mono_class_from_name || !mono_class_get_method_from_name ||
        !mono_string_new || !mono_domain_get || !mono_runtime_invoke) return false;
    MonoClass* layer = mono_class_from_name(AppSystem_img, "Sce.Vsh.ShellUI.AppSystem", "LayerManager");
    if (!layer) return false;
    MonoMethod* find = mono_class_get_method_from_name(layer, "FindContainerSceneByPath", 1);
    if (!find) return false;
    MonoString* path = mono_string_new(mono_domain_get(), "Game");
    void* args[1] = { path };
    MonoObject* exception = nullptr;
    MonoObject* scene = mono_runtime_invoke(find, nullptr, args, &exception);
    if (exception || !scene) return false;
    Game = scene;
    return true;
}

void OnRender_Hook(MonoObject* instance)
{
    static bool Do_Once = false;
    static unsigned int Idle_Thread_ID[8];
    static int Current_Bank = 0;

    // Separate labels for text and values
    static MonoObject* gpu_temp_value = nullptr;
    static MonoObject* gpu_usage_value = nullptr;

    static MonoObject* cpu_temp_value = nullptr;
    static MonoObject* cpu_usage_value = nullptr;

    static MonoObject* ram_value = nullptr;
    static MonoObject* fps_value = nullptr;


    char GPU_TEMP[32];
    char GPU_USAGE[32];
    char CPU_TEMP[32];
    char CPU_USAGE[120];
    char RAM_STR[32];

    static int wait = 0;
    int SOC_temp = 0;
    int CPU_temp = 0;

    // FIX70.33 service-only mode: consume web controls on the PUI Update
    // callback and apply overlay changes on ShellUI's managed thread.
    if (g_pizzahen_shell_service_mode) {
        static unsigned int control_tick = 0;
        if (++control_tick >= 2) { control_tick = 0; PizzahenServiceWebControl(); }

        const int bigapp_id = sceSystemServiceGetAppIdOfRunningBigApp ?
            sceSystemServiceGetAppIdOfRunningBigApp() : -1;
        if (bigapp_id != g_pizzahen_service_bigapp_id) {
            g_pizzahen_service_bigapp_id = bigapp_id;
            Game = nullptr;
            rootWidget = nullptr;
            Do_Once = false;
            g_pizzahen_overlay_apply_requested = true;
        }

        const bool want_overlay = global_conf.overlay_cpu || global_conf.all_cpu_usage ||
                                  global_conf.overlay_ram || global_conf.overlay_gpu ||
                                  global_conf.overlay_fps || global_conf.overlay_ip;
        if ((g_pizzahen_overlay_apply_requested || want_overlay) && !pizzahen_resolve_game_scene()) {
            OnRender_orig(instance);
            return;
        }
        if (g_pizzahen_overlay_apply_requested) {
            RemoveGameWidget(REMOVE_ALL_OVERLAYS);
            Do_Once = false;
            g_pizzahen_overlay_apply_requested = false;
        }
        if (!want_overlay) {
            OnRender_orig(instance);
            return;
        }
    }

    if (!Do_Once)
    {
#if 1
        fps_string.store("LOADING");
#else
        fps_string.store("NOT SUPPORTED IN THIS BUILD");
#endif
	//	shellui_log("string %s", fps_string.load().c_str());
        int Thread_Count = 3072;
        if (!sceKernelGetCpuUsage((Proc_Stats*)&Stat_Data, (int*)&Thread_Count) && Thread_Count > 0)
        {
            char Thread_Name[0x40];
            int Core_Count = 0;
            for (int i = 0; i < Thread_Count; i++)
            {
                if (!sceKernelGetThreadName(Stat_Data[i].td_tid, Thread_Name) && sscanf(Thread_Name, "SceIdleCpu%d", &Core_Count) == 1 && Core_Count <= 7)
                {
                    Idle_Thread_ID[Core_Count] = Stat_Data[i].td_tid;
                }
            }
        }

        rootWidget = Get_Property<MonoObject*>(pui_img, "Sce.PlayStation.PUI.UI2", "Scene", Game, "RootWidget");
        font = CreateUIFont(22, 0, 0);           // Regular font for values

        // GPU row - Green label (BOLD), Orange values - Better spacing
        if (global_conf.overlay_cpu) {
            CreateGameWidget(CREATE_CPU_OVERLAY);
        }
        if (global_conf.overlay_ram) {
            CreateGameWidget(CREATE_RAM_OVERLAY);
        }
        if (global_conf.overlay_gpu) {
            CreateGameWidget(CREATE_GPU_OVERLAY);
        }
        if (global_conf.overlay_fps) {
            CreateGameWidget(CREATE_FPS_OVERLAY);
        }
		if (global_conf.overlay_ip) {
			CreateGameWidget(CREATE_IP_OVERLAY);
		}

        Do_Once = true;
    }


    if (wait <= 0) {


        // Get CPU usage
        while (global_conf.overlay_cpu || global_conf.all_cpu_usage) {
            gThread_Data[Current_Bank].Thread_Count = 3072;
            if (!sceKernelGetCpuUsage((Proc_Stats*)&gThread_Data[Current_Bank].Threads, &gThread_Data[Current_Bank].Thread_Count))
            {
                Thread_Count = gThread_Data[Current_Bank].Thread_Count;
                sceKernelClockGettime(4, &gThread_Data[Current_Bank].current_time);
                Current_Bank = !Current_Bank;

                if (gThread_Data[Current_Bank].Thread_Count <= 0)
                    continue;

                calc_usage(Idle_Thread_ID, &gThread_Data[!Current_Bank], &gThread_Data[Current_Bank], Usage);

                if (global_conf.all_cpu_usage) {
                    snprintf(CPU_USAGE, sizeof(CPU_USAGE), "%2.0f%% %2.0f%% %2.0f%% %2.0f%% %2.0f%% %2.0f%% %2.0f%% %2.0f%%",Usage[0], Usage[1], Usage[2], Usage[3], Usage[4], Usage[5], Usage[6], Usage[7]);
                    break;
                }

                // Calculate average CPU usage
                float avg_cpu = 0;
                for (int i = 0; i < 8; i++) {
                    avg_cpu += Usage[i];
                }
                avg_cpu /= 8.0f;

                snprintf(CPU_USAGE, sizeof(CPU_USAGE), "%.0f%%", avg_cpu);
                break;
            }
        }

        // Get RAM info
        if (global_conf.overlay_ram)
        {
            Get_Page_Table_Stats(1, 1, &RAM.Used, &RAM.Free, &RAM.Total);
            snprintf(RAM_STR, sizeof(RAM_STR), "%u MB", RAM.Used);
        }

        // Get GPU usage (estimate based on VRAM usage)
        if (global_conf.overlay_gpu) 
        {
            // Get temperatures
            sceKernelGetSocSensorTemperature(0, &SOC_temp);
            snprintf(GPU_TEMP, sizeof(GPU_TEMP), "%dC", SOC_temp);
            Get_Page_Table_Stats(1, 2, &VRAM.Used, &VRAM.Free, &VRAM.Total);
            VRAM.Percentage = (((float)VRAM.Used / (float)VRAM.Total) * 100.0f);
            snprintf(GPU_USAGE, sizeof(GPU_USAGE), "%.0f%%", VRAM.Percentage);
        }
        if(global_conf.overlay_ip)
        {
			char ip_address[64];
            get_ip_address(&ip_address[0]);
            MonoObject* ip_value = Invoke<MonoObject*>(pui_img, mono_class_from_name(pui_img, "Sce.PlayStation.PUI.UI2", "Widget"), Get_Property<MonoObject*>(pui_img, "Sce.PlayStation.PUI.UI2", "Scene", Game, "RootWidget"), "FindWidgetByName", mono_string_new(Root_Domain, "id_ip_value"));
            Set_Property(mono_class_from_name(pui_img, "Sce.PlayStation.PUI.UI2", "Label"), ip_value, "Text", mono_string_new(Root_Domain, ip_address));
		}

        if (global_conf.overlay_gpu) {
            // Update GPU values
            gpu_temp_value = Invoke<MonoObject*>(pui_img, mono_class_from_name(pui_img, "Sce.PlayStation.PUI.UI2", "Widget"), Get_Property<MonoObject*>(pui_img, "Sce.PlayStation.PUI.UI2", "Scene", Game, "RootWidget"), "FindWidgetByName", mono_string_new(Root_Domain, "id_gpu_temp_value"));
            Set_Property(mono_class_from_name(pui_img, "Sce.PlayStation.PUI.UI2", "Label"), gpu_temp_value, "Text", mono_string_new(Root_Domain, GPU_TEMP));

            gpu_usage_value = Invoke<MonoObject*>(pui_img, mono_class_from_name(pui_img, "Sce.PlayStation.PUI.UI2", "Widget"), Get_Property<MonoObject*>(pui_img, "Sce.PlayStation.PUI.UI2", "Scene", Game, "RootWidget"), "FindWidgetByName", mono_string_new(Root_Domain, "id_gpu_usage_value"));
            Set_Property(mono_class_from_name(pui_img, "Sce.PlayStation.PUI.UI2", "Label"), gpu_usage_value, "Text", mono_string_new(Root_Domain, GPU_USAGE));
        }
        if (global_conf.overlay_cpu || global_conf.all_cpu_usage) {
            sceKernelGetCpuTemperature(&CPU_temp);
            // Format temperature strings
            snprintf(CPU_TEMP, sizeof(CPU_TEMP), "%dC", CPU_temp);
            // Update CPU values
            cpu_temp_value = Invoke<MonoObject*>(pui_img, mono_class_from_name(pui_img, "Sce.PlayStation.PUI.UI2", "Widget"), Get_Property<MonoObject*>(pui_img, "Sce.PlayStation.PUI.UI2", "Scene", Game, "RootWidget"), "FindWidgetByName", mono_string_new(Root_Domain, "id_cpu_temp_value"));
            Set_Property(mono_class_from_name(pui_img, "Sce.PlayStation.PUI.UI2", "Label"), cpu_temp_value, "Text", mono_string_new(Root_Domain, CPU_TEMP));

            cpu_usage_value = Invoke<MonoObject*>(pui_img, mono_class_from_name(pui_img, "Sce.PlayStation.PUI.UI2", "Widget"), Get_Property<MonoObject*>(pui_img, "Sce.PlayStation.PUI.UI2", "Scene", Game, "RootWidget"), "FindWidgetByName", mono_string_new(Root_Domain, "id_cpu_usage_value"));
            Set_Property(mono_class_from_name(pui_img, "Sce.PlayStation.PUI.UI2", "Label"), cpu_usage_value, "Text", mono_string_new(Root_Domain, CPU_USAGE));
        }
        if(global_conf.overlay_ram) 
        {
            // Update RAM value
            ram_value = Invoke<MonoObject*>(pui_img, mono_class_from_name(pui_img, "Sce.PlayStation.PUI.UI2", "Widget"), Get_Property<MonoObject*>(pui_img, "Sce.PlayStation.PUI.UI2", "Scene", Game, "RootWidget"), "FindWidgetByName", mono_string_new(Root_Domain, "id_ram_value"));
            Set_Property(mono_class_from_name(pui_img, "Sce.PlayStation.PUI.UI2", "Label"), ram_value, "Text", mono_string_new(Root_Domain, RAM_STR));
		}
        if (global_conf.overlay_fps) {
            // Update FPS value
            std::string current_fps = fps_string.load();
            fps_value = Invoke<MonoObject*>(pui_img, mono_class_from_name(pui_img, "Sce.PlayStation.PUI.UI2", "Widget"), Get_Property<MonoObject*>(pui_img, "Sce.PlayStation.PUI.UI2", "Scene", Game, "RootWidget"), "FindWidgetByName", mono_string_new(Root_Domain, "id_fps_value"));
            Set_Property(mono_class_from_name(pui_img, "Sce.PlayStation.PUI.UI2", "Label"), fps_value, "Text", mono_string_new(Root_Domain, current_fps.c_str()));
        }
        wait = 60; // Update every 60 frames
    }
    else {
        wait--;
    }

    OnRender_orig(instance);
}



int (*sceAppInstUtilInstallByPackage_orig)(MetaInfo* arg1, SceAppInstallPkgInfo* pkg_info, PlayGoInfo* arg2) = nullptr;
void hex_dump(const char* label, const void* data, size_t size) {
    const unsigned char* bytes = (const unsigned char*)data;
    shellui_log("=== %s (size: %zu bytes) ===", label, size);

    for (size_t i = 0; i < size; i += 16) {
        char line[128];
        int offset = 0;

        // Print offset
        offset += snprintf(line + offset, sizeof(line) - offset,
            "%04zx: ", i);

        // Print hex values
        for (size_t j = 0; j < 16; j++) {
            if (i + j < size) {
                offset += snprintf(line + offset, sizeof(line) - offset,
                    "%02x ", bytes[i + j]);
            }
            else {
                offset += snprintf(line + offset, sizeof(line) - offset,
                    "   ");
            }
        }

        // Print ASCII representation
        offset += snprintf(line + offset, sizeof(line) - offset, " |");
        for (size_t j = 0; j < 16 && i + j < size; j++) {
            unsigned char c = bytes[i + j];
            offset += snprintf(line + offset, sizeof(line) - offset,
                "%c", (c >= 32 && c <= 126) ? c : '.');
        }
        offset += snprintf(line + offset, sizeof(line) - offset, "|");

        shellui_log("%s", line);
    }
}
extern "C" int sceAppInstUtilInitialize();

int sceAppInstUtilInstallByPackage_hook(MetaInfo* arg1,
    SceAppInstallPkgInfo* pkg_info,
    PlayGoInfo* arg2) {

    shellui_log("========== sceAppInstUtilInstallByPackage_hook ==========");

    sceAppInstUtilInitialize();

    // Print MetaInfo
    if (arg1) {
        shellui_log("--- MetaInfo ---");
        shellui_log("uri: %s", arg1->uri ? arg1->uri : "(null)");
        shellui_log("ex_uri: %s", arg1->ex_uri ? arg1->ex_uri : "(null)");
        shellui_log("playgo_scenario_id: %s",
            arg1->playgo_scenario_id ? arg1->playgo_scenario_id : "(null)");
        shellui_log("content_id: %s",
            arg1->content_id ? arg1->content_id : "(null)");
        shellui_log("content_name: %s",
            arg1->content_name ? arg1->content_name : "(null)");
        shellui_log("icon_url: %s",
            arg1->icon_url ? arg1->icon_url : "(null)");
    }
    else {
        shellui_log("MetaInfo: (null)");
    }

    // Print SceAppInstallPkgInfo
    if (pkg_info) {
        shellui_log("--- SceAppInstallPkgInfo ---");
        shellui_log("content_id: %.*s", CONTENTID_SIZE, pkg_info->content_id);
        shellui_log("content_type: %d", pkg_info->content_type);
        shellui_log("content_platform: %d", pkg_info->content_platform);
    }
    else {
        shellui_log("SceAppInstallPkgInfo: (null)");
    }

    // Print PlayGoInfo
    if (arg2) {
        shellui_log("--- PlayGoInfo ---");

        // Print languages
        shellui_log("Languages:");
        for (int i = 0; i < NUM_LANGUAGES; i++) {
            if (arg2->languages[i][0] != '\0') {
                shellui_log("  [%d]: %.*s", i, LANGUAGE_SIZE,
                    arg2->languages[i]);
            }
        }

        // Print playgo_scenario_ids
        shellui_log("PlayGo Scenario IDs:");
        for (int i = 0; i < NUM_IDS; i++) {
            if (arg2->playgo_scenario_ids[i][0] != '\0') {
                shellui_log("  [%d]: %.*s", i, PLAYGOSCENARIOID_SIZE,
                    arg2->playgo_scenario_ids[i]);
            }
        }

        // Print content_ids
        shellui_log("Content IDs:");
        for (int i = 0; i < NUM_IDS; i++) {
            if (arg2->content_ids[i][0] != '\0') {
                shellui_log("  [%d]: %.*s", i, CONTENTID_SIZE,
                    arg2->content_ids[i]);
            }
        }

        // Hex dump unknown portion
        hex_dump("PlayGoInfo::unknown", arg2->unknown,
            sizeof(arg2->unknown));
    }
    else {
        shellui_log("PlayGoInfo: (null)");
    }

    shellui_log("========== Calling Original Function ==========");
    notify("Installing package from:\n%s",
        arg1 ? (arg1->uri ? arg1->uri : "(null)") : "(null)");

    int ret = sceAppInstUtilInstallByPackage_orig(arg1, pkg_info, arg2);

    shellui_log("sceAppInstUtilInstallByPackage_hook returned: %d", ret);
    notify("Installation finished with code: %d", ret);

    return ret;
}
bool is_6xx = false, is_3xx = false;

void* dialogue_thread(void* arg) {
    bool selector_opened = false;
    while (true) {
        usleep(250 * 1000);
        const bool selector_active = if_exists("/system_tmp/pizzahen_kstuff_selector_active");
        if (selector_active && !selector_opened) {
            shellui_log("FIX23: opening PIZZA HEN KStuff selector");
            GoToURI(pizzahen_debug_services_uri());
            touch_file("/system_tmp/pizzahen_kstuff_selector_ui_opened");
            selector_opened = true;
        } else if (!selector_active && selector_opened) {
            unlink("/system_tmp/pizzahen_kstuff_selector_ui_opened");
            selector_opened = false;
        }
    }
    return nullptr;
}
int main(int argc, char const *argv[]) {
  OrbisKernelSwVersion sw;
  char buz[100];
  if (hooked) {
    return 0;
  }

  // OnionHEN hook transaction: every callback stays pass-through until the
  // complete ShellUI hook set for this invocation has committed.
  shellui_hooks_begin_install();

  static ssize_t(*read)(int fd, void* buf, size_t count) = nullptr;
  static int (*sceAppInstUtilInstallByPackage)(MetaInfo * arg1, SceAppInstallPkgInfo * pkg_info, PlayGoInfo * arg2) = nullptr;


  pid_t pid = getpid();
  uintptr_t old_authid = set_ucred_to_debugger();


  int appinstaller_handle = get_module_handle(pid, "libSceAppInstUtil.sprx");
  KERNEL_DLSYM(appinstaller_handle, sceAppInstUtilInstallByPackage);
  

  int libkernelsys_handle = get_module_handle(pid, "libkernel_sys.sprx");

  KERNEL_DLSYM(libkernelsys_handle, sceKernelDebugOutText);
  KERNEL_DLSYM(libkernelsys_handle, sceKernelMkdir);
  KERNEL_DLSYM(libkernelsys_handle, scePthreadCreate);
  KERNEL_DLSYM(libkernelsys_handle, sceKernelMprotect);
  KERNEL_DLSYM(libkernelsys_handle, sceKernelSendNotificationRequest);
  KERNEL_DLSYM(libkernelsys_handle, sceKernelGetProsperoSystemSwVersion);
  KERNEL_DLSYM(libkernelsys_handle, sceKernelGetAppInfo);
  KERNEL_DLSYM(libkernelsys_handle, sceKernelGetProcessName);
  KERNEL_DLSYM(libkernelsys_handle, read);

  shellui_log("Starting ShellUI Module ....");
  // int native_handle = get_module_handle(pid, "libNativeExtensions.sprx");
  //KERNEL_DLSYM(native_handle, DecryptRnpsBundle);
  
  // KERNEL_DLSYM(libSceKernelHandle, sceKernelGetSocSensorTemperature);
  //
  //  JIT
  //
  KERNEL_DLSYM(libSceKernelHandle, sceKernelJitCreateSharedMemory);
  KERNEL_DLSYM(libSceKernelHandle, sceKernelJitCreateAliasOfSharedMemory);
  KERNEL_DLSYM(libSceKernelHandle, sceKernelJitMapSharedMemory);
  KERNEL_DLSYM(libSceKernelHandle, ioctl);
  KERNEL_DLSYM(libSceKernelHandle, __sys_regmgr_call);

  // get the yscall address for the ioctl hook
  static __attribute__ ((used)) long getpid = 0;
  KERNEL_DLSYM(libSceKernelHandle, getpid);
  ptr_syscall = getpid;
  ptr_syscall += 0xa; // jump directly to the syscall instruction

  int libshelluiutil_handle = get_module_handle(pid, "libSceShellUIUtil.sprx");
  KERNEL_DLSYM(libshelluiutil_handle, sceShellUIUtilLaunchByUri);
  KERNEL_DLSYM(libshelluiutil_handle, sceShellUIUtilInitialize);
  

  //
  // Mono is already loaded into the SceShellUI process
  //
  int libmono_handle = get_module_handle(pid, "libmonosgen-2.0.sprx");

  KERNEL_DLSYM(libmono_handle, mono_object_to_string);
  KERNEL_DLSYM(libmono_handle, mono_get_root_domain);
  KERNEL_DLSYM(libmono_handle, mono_property_get_get_method);
  KERNEL_DLSYM(libmono_handle, mono_property_get_set_method);
  KERNEL_DLSYM(libmono_handle, mono_class_get_property_from_name);
  KERNEL_DLSYM(libmono_handle, mono_class_from_name);
  KERNEL_DLSYM(libmono_handle, mono_raise_exception);
  KERNEL_DLSYM(libmono_handle, mono_runtime_invoke);
  KERNEL_DLSYM(libmono_handle, mono_array_new);
  KERNEL_DLSYM(libmono_handle, mono_string_new);
  KERNEL_DLSYM(libmono_handle, mono_jit_set_aot_only);
  KERNEL_DLSYM(libmono_handle, mono_jit_init_version);
  KERNEL_DLSYM(libmono_handle, mono_object_new);
  KERNEL_DLSYM(libmono_handle, mono_object_unbox);
  KERNEL_DLSYM(libmono_handle, mono_set_dirs);
  KERNEL_DLSYM(libmono_handle, mono_compile_method);
  KERNEL_DLSYM(libmono_handle, mono_assembly_get_image);
  KERNEL_DLSYM(libmono_handle, mono_domain_assembly_open);
  KERNEL_DLSYM(libmono_handle, mono_get_byte_class);
  KERNEL_DLSYM(libmono_handle, mono_thread_attach);
  KERNEL_DLSYM(libmono_handle, mono_object_get_class);
  KERNEL_DLSYM(libmono_handle, mono_vtable_get_static_field_data);
  KERNEL_DLSYM(libmono_handle, mono_class_get_method_from_name);
  KERNEL_DLSYM(libmono_handle, mono_class_get_field_from_name);
  KERNEL_DLSYM(libmono_handle, mono_aot_get_method);
  KERNEL_DLSYM(libmono_handle, mono_field_static_set_value);
  KERNEL_DLSYM(libmono_handle, mono_assembly_setrootdir);
  KERNEL_DLSYM(libmono_handle, mono_free);
  KERNEL_DLSYM(libmono_handle, mono_gchandle_new);
  KERNEL_DLSYM(libmono_handle, mono_image_open_from_data);
  KERNEL_DLSYM(libmono_handle, mono_runtime_object_init);
  KERNEL_DLSYM(libmono_handle, mono_domain_get);
  KERNEL_DLSYM(libmono_handle, mono_assembly_load_from);
  KERNEL_DLSYM(libmono_handle, mono_method_desc_new);
  KERNEL_DLSYM(libmono_handle, mono_method_desc_search_in_class);
  KERNEL_DLSYM(libmono_handle, mono_method_desc_free);
  KERNEL_DLSYM(libmono_handle, mono_object_new_specific);
  KERNEL_DLSYM(libmono_handle, mono_thread_detach);
  KERNEL_DLSYM(libmono_handle, mono_array_addr_with_size);
  KERNEL_DLSYM(libmono_handle, mono_thread_current);
  KERNEL_DLSYM(libmono_handle, mono_class_vtable);
  KERNEL_DLSYM(libmono_handle, mono_domain_unload);
  KERNEL_DLSYM(libmono_handle, mono_string_to_utf8);

  // R7.3: FIX70.37 already proved that a service-only ShellUI consumer must
  // not require the complete legacy Settings Mono surface.  The Game Options
  // service needs only assembly lookup + method compilation + strings.
  const bool shell_service_requested =
      if_exists("/system_tmp/pizzahen_shell_service_mode");
  const bool game_options_service_requested = shell_service_requested;
  [[maybe_unused]] const bool game_options_mono_ready =
      mono_get_root_domain && mono_thread_attach && mono_domain_get &&
      mono_domain_assembly_open && mono_assembly_get_image &&
      mono_class_from_name && mono_class_get_method_from_name && mono_compile_method &&
      mono_string_new && mono_string_to_utf8 && mono_free;

  const bool full_mono_ready =
      mono_object_to_string && mono_get_root_domain &&
      mono_property_get_get_method && mono_property_get_set_method &&
      mono_class_get_property_from_name && mono_class_from_name &&
      mono_runtime_invoke && mono_array_new && mono_string_new &&
      mono_jit_set_aot_only && mono_jit_init_version && mono_object_new &&
      mono_object_unbox && mono_set_dirs && mono_compile_method &&
      mono_assembly_get_image && mono_domain_assembly_open &&
      mono_get_byte_class && mono_thread_attach && mono_object_get_class &&
      mono_vtable_get_static_field_data && mono_class_get_method_from_name &&
      mono_class_get_field_from_name && mono_aot_get_method &&
      mono_field_static_set_value && mono_assembly_setrootdir && mono_free &&
      mono_gchandle_new && mono_image_open_from_data &&
      mono_runtime_object_init && mono_domain_get &&
      mono_assembly_load_from && mono_method_desc_new &&
      mono_method_desc_search_in_class && mono_method_desc_free &&
      mono_object_new_specific && mono_thread_detach &&
      mono_array_addr_with_size && mono_thread_current &&
      mono_class_vtable && mono_domain_unload && mono_string_to_utf8;

  if (shell_service_requested ? !full_mono_ready : !full_mono_ready) {
    shellui_log("Failed to resolve %s Mono symbols",
                shell_service_requested ? "Shell service" : "full");
    return -1;
  }

  int libscesystem_service_handle =
      get_module_handle(pid, "libSceSystemService.sprx");

  KERNEL_DLSYM(libscesystem_service_handle,
               sceSystemServiceGetAppIdOfRunningBigApp);
  KERNEL_DLSYM(libscesystem_service_handle, sceSystemServiceGetAppTitleId);


  void *sceSystemServiceLaunchApp = nullptr;
  KERNEL_DLSYM(libscesystem_service_handle, sceSystemServiceLaunchApp);
  if (!sceSystemServiceLaunchApp) {
    shellui_log("Failed to resolve sceSystemServiceLaunchApp");
  }

  int libRemotePlay_handle = get_module_handle(pid, "libSceRemoteplay.sprx");

  KERNEL_DLSYM(libRemotePlay_handle, sceRemoteplayNotifyPinCodeError);
  KERNEL_DLSYM(libRemotePlay_handle, sceRemoteplayInitialize);
  KERNEL_DLSYM(libRemotePlay_handle, sceRemoteplayGeneratePinCode);
  KERNEL_DLSYM(libRemotePlay_handle, sceRemoteplayConfirmDeviceRegist);

  
  int libReg_handle = get_module_handle(pid, "libSceRegMgr.sprx");
  KERNEL_DLSYM(libReg_handle, sceRegMgrGetInt);

  /*
  "Sce.Vsh.UILib", "SystemSoftwareVersionInfo");
  */
  std::string SettingsPage_dec = base64_decode("U2V0dGluZ1BhZ2U=");
  std::string SettingsPlugin_dec = base64_decode("U2V0dGluZ3NQbHVnaW4=");
  std::string cxml_dec = base64_decode("Q3htbFVyaQ==");
  std::string GetManifestResourceStream_dec = base64_decode("R2V0TWFuaWZlc3RSZXNvdXJjZVN0cmVhbQ==");
  std::string RuntimeAssembly_dec = base64_decode("UnVudGltZUFzc2VtYmx5");
  std::string sys_reflection_dec = base64_decode("U3lzdGVtLlJlZmxlY3Rpb24==");
  std::string key_base64 = "U0lTVFIwX0lfU0VFX1lPVQ==";
  legacy_dec = base64_decode("U2NlLlZzaC5TaGVsbFVJLkxlZ2FjeS5kbGw=");
  UI3_dec = base64_decode("U2NlLlZzaC5TaGVsbFVJLlNldHRpbmdzLkNvcmVVSTM=");
  plugin_xml = base64_decode("U2NlLlZzaC5TaGVsbFVJLkxlZ2FjeS5zcmMuU2NlLlZzaC5Ta"
                             "GVsbFVJLlNldHRpbmdzLlBsdWdpbnMucGx1Z2lucy54bWw=");
  cheats_xml = base64_decode("U2NlLlZzaC5TaGVsbFVJLkxlZ2FjeS5zcmMuU2NlLlZzaC5Ta"
                             "GVsbFVJLlNldHRpbmdzLlBsdWdpbnMuY2hlYXRzLnhtbA==");
  remote_play_xml =  base64_decode("U2NlLlZzaC5TaGVsbFVJLkxlZ2FjeS5zcmMuU2NlLlZzaC5TaGVsbFVJLlNldHRpbmdzLlBsdWdpbnMucmVtb3RlX3BsYXkueG1s");
  debug_settings_xml = base64_decode(
      "U2NlLlZzaC5TaGVsbFVJLkxlZ2FjeS5zcmMuU2NlLlZzaC5TaGVsbFVJLlNldHRpbmdzLlBs"
      "dWdpbnMuRGVidWdTZXR0aW5ncy5kYXRhLmRlYnVnX3NldHRpbmdzLnhtbA==");
  appsystem_dll = base64_decode("U2NlLlZzaC5TaGVsbFVJLkFwcFN5c3RlbS5kbGw=");
  uilib = base64_decode("U2NlLlZzaC5VSUxpYg==");
  Sysinfo = base64_decode("U3lzdGVtU29mdHdhcmVWZXJzaW9uSW5mbw==");
  display_info = base64_decode("c2V0X0Rpc3BsYXlWZXJzaW9u");
  uilib_dll = base64_decode("L3N5c3RlbV9leC9jb21tb25fZXgvbGliL1NjZS5Wc2guVUlMaWIuZGxs");

  // Base64 decoded strings
  std::string mscorlib_dll = base64_decode("bXNjb3JsaWIuZGxs"); // "mscorlib.dll"
  std::string reactpui_dll = base64_decode("UmVhY3ROYXRpdmUuUFVJLmRsbA=="); // "ReactNative.PUI.dll"
  std::string appsystem_dll_name = base64_decode("U2NlLlZzaC5TaGVsbFVJLkFwcFN5c3RlbS5kbGw="); // "Sce.Vsh.ShellUI.AppSystem.dll"
  std::string core_dll = base64_decode("U2NlLlBsYXlTdGF0aW9uLkNvcmUuZGxs"); // "Sce.PlayStation.Core.dll"
  std::string capture_menu_dll = base64_decode("U2NlLlZzaC5TaGVsbFVJLkNhcHR1cmVNZW51LmRsbA=="); // "Sce.Vsh.ShellUI.CaptureMenu.dll"

  // Namespace and class names
  std::string appsystem_namespace = base64_decode("U2NlLlZzaC5TaGVsbFVJLkFwcFN5c3RlbQ=="); // "Sce.Vsh.ShellUI.AppSystem"
  std::string layer_manager = base64_decode("TGF5ZXJNYW5hZ2Vy"); // "LayerManager"
  std::string update_impose_flag = base64_decode("VXBkYXRlSW1wb3NlU3RhdHVzRmxhZw=="); // "UpdateImposeStatusFlag"
  std::string input_namespace = base64_decode("U2NlLlBsYXlTdGF0aW9uLkNvcmUuSW5wdXQ="); // "Sce.PlayStation.Core.Input"
  std::string gamepad_class = base64_decode("R2FtZVBhZA=="); // "GamePad"
  std::string getdata_method = base64_decode("R2V0RGF0YQ=="); // "GetData"
  std::string security_namespace = base64_decode("UmVhY3ROYXRpdmUuUGxheVN0YXRpb24uU2VjdXJpdHk="); // "ReactNative.PlayStation.Security" 
  std::string bundle_decryptor = base64_decode("SmF2YVNjcmlwdEJ1bmRsZURlY3J5cHRvcg=="); // "JavaScriptBundleDecryptor"
  std::string decrypt_method = base64_decode("RGVjcnlwdA=="); // "Decrypt"
  std::string onpressed_method = base64_decode("T25QcmVzc2Vk"); // "OnPressed"
  std::string boot_helper = base64_decode("Qm9vdEhlbHBlcg=="); // "BootHelper"
  std::string boot_method = base64_decode("Qm9vdA=="); // "Boot"
  std::string capture_namespace = base64_decode("U2NlLlZzaC5TaGVsbFVJLkNhcHR1cmVNZW51"); // "Sce.Vsh.ShellUI.CaptureMenu"
  std::string capture_controller = base64_decode("Q2FwdHVyZUNvbnRyb2xsZXI="); // "CaptureController"
  std::string capture_screen = base64_decode("Q2FwdHVyZVNjcmVlbg=="); // "CaptureScreen"
  std::string event_manager = base64_decode("RXZlbnRNYW5hZ2Vy"); // "EventManager" 
  std::string onshare_button = base64_decode("T25TaGFyZUJ1dHRvbg=="); // "OnShareButton"
  std::string oncreating_method = base64_decode("T25DcmVhdGluZw=="); // "OnCreating"
  std::string getstring_method = base64_decode("R2V0U3RyaW5n"); // "GetString"
  std::string term = base64_decode("VGVybWluYXRl"); // "Terminate"

  sceKernelGetProsperoSystemSwVersion(&sw);
  is_3xx = (sw.version < 0x4000042);
  is_6xx = (sw.version >= 0x6000000);
  pizzahen_configure_debug_services_route(sw.version);
  shellui_log("System Software Version: %s is_3xx: %s DebugServicesRoute: %s",
              sw.version_str, is_3xx ? "Yes" : "No",
              pizzahen_debug_services_uses_old_route() ? "debug_settings_old" : "debug_settings");

#if 0
  sceLncUtilLaunchApp_dyn = reinterpret_cast<SceLncUtilLaunchAppType>(reinterpret_cast<uintptr_t>(sceSystemServiceLaunchApp) + is_3xx ? 0x1250 : 0x1260));
#endif

  if (mono_get_root_domain) {
    shellui_log("loading settings");
    if (!LoadSettings()) {
      shellui_log("Failed to load settings");
      return -1;
    } else {
      shellui_log("Settings loaded successfully");
    }

    // R7.5: Debug Services must not resurrect the legacy etaHEN/ShellUI
    // performance overlays from persisted config.  The startup Game Options
    // service is intentionally excluded.  This does NOT touch the separate
    // PHU Overlay payload or /data/phu_overlay.lock owned by the PIZZA Toolbox.
    if (!game_options_service_requested) {
      global_conf.overlay_ram = false;
      global_conf.overlay_cpu = false;
      global_conf.overlay_gpu = false;
      global_conf.overlay_fps = false;
      global_conf.overlay_ip = false;
      global_conf.overlay_kstuff = false;
      global_conf.overlay_kstuff_active = false;
      global_conf.all_cpu_usage = false;
      unlink("/system_tmp/fps_enabled");
      shellui_log("PIZZA HEN R7.5: Debug Services legacy overlays forced OFF; PHU Overlay untouched");
    }

    Root_Domain = mono_get_root_domain();
    if (!Root_Domain) {
      shellui_log( "failed to get shellui root domain");
      return -1;
    } else {
      shellui_log("Shellui Root Domain: %p", Root_Domain);
    }

    mono_thread_attach(Root_Domain);

    // R7.5.3: restore the FIX70.33 source-grounded lazy Shell service.
    // It is started only on demand from the Toolbox, never immediately after
    // KStuff selection. Debug Services remains a separate launcher/path.
    if (shell_service_requested) {
      static const char *PIZZAHEN_SHELL_SERVICE_ONLINE = "/system_tmp/pizzahen_shell_service_online";
      static const char *PIZZAHEN_SHELL_SERVICE_PID = "/system_tmp/pizzahen_shell_service_pid";
      g_pizzahen_shell_service_mode = true;

      AppSystem_img = getDLLimage(appsystem_dll_name.c_str());
      pui_img = getDLLimage("Sce.PlayStation.PUI.dll");
      if (!AppSystem_img || !pui_img) {
        shellui_log("PIZZA HEN R7.5.3: Shell service missing AppSystem/PUI");
        unlink(PIZZAHEN_SHELL_SERVICE_ONLINE);
        set_proc_authid(pid, old_authid);
        return -1;
      }
      Game = nullptr;

      const uint64_t service_on_render = Get_Address_of_Method(
          pui_img, "Sce.PlayStation.PUI", "Application", "Update", 0);
      if (!service_on_render) {
        shellui_log("PIZZA HEN R7.5.3: PUI Application.Update unavailable");
        unlink(PIZZAHEN_SHELL_SERVICE_ONLINE);
        set_proc_authid(pid, old_authid);
        return -1;
      }
      OnRender_orig = (void(*)(MonoObject*))DetourFunction(service_on_render, (void*)&OnRender_Hook);
      if (!OnRender_orig) {
        shellui_log("PIZZA HEN R7.5.3: PUI service Update detour failed");
        unlink(PIZZAHEN_SHELL_SERVICE_ONLINE);
        set_proc_authid(pid, old_authid);
        return -1;
      }

      // Curated handlers from FIX70.33: registry Title IDs, KStuff game
      // lifecycle, controller shortcuts and Game Options. Missing optional
      // images do not take down the mandatory web-control/overlay consumer.
      MonoImage *service_core = getDLLimage(core_dll.c_str());
      MonoImage *service_capture = getDLLimage(capture_menu_dll.c_str());
      MonoImage *service_lnc = getDLLimage("Sce.Vsh.LncUtilWrapper.dll");
      react_common_img = getDLLimage("ReactNative.Vsh.Common.dll");
      MonoImage *service_react_shell = getDLLimage("Sce.Vsh.ShellUI.ReactNativeShellApp.dll");
      MonoImage *service_react_pui = getDLLimage(reactpui_dll.c_str());
      const bool service_string_api = (mono_string_to_utf8 && mono_free);

      if (sceRegMgrGetInt) {
        auto regmgr_trampoline = (int(*)(long, int*))DetourFunction(
            (uintptr_t)sceRegMgrGetInt, (void*)&sceRegMgrGetInt_hook);
        if (regmgr_trampoline) sceRegMgrGetInt = regmgr_trampoline;
      }
      if (service_lnc && service_string_api) {
        const uint64_t launch_method = Get_Address_of_Method(
            service_lnc, "Sce.Vsh.LncUtil", "LncUtilWrapper", "LaunchApp", 4);
        if (launch_method)
          LaunchApp_orig = (int(*)(MonoString*, uint64_t*, int, LaunchAppParam*))
              DetourFunction(launch_method, (void*)&LaunchApp);
        const uint64_t kill_method = Get_Address_of_Method(
            service_lnc, "Sce.Vsh.LncUtil", "LncUtilWrapper", "KillAppWithReason", 2);
        if (kill_method) (void)DetourFunction(kill_method, (void*)&KillAppWithReason_Hook);
      }
      if (service_core) {
        const uint64_t gamepad_method = Get_Address_of_Method(
            service_core, input_namespace.c_str(), gamepad_class.c_str(), getdata_method.c_str(), 1);
        if (gamepad_method)
          GetData = (GamePadData(*)(int))DetourFunction(gamepad_method, (void*)&GetData_hook);
      }
      if (service_capture) {
        const uint64_t capture4 = Get_Address_of_Method(
            service_capture, capture_namespace.c_str(), capture_controller.c_str(), capture_screen.c_str(), 4);
        if (capture4)
          CaptureScreen_orig_old = (void(*)(MonoObject*, int, long, int, MonoObject*))
              DetourFunction(capture4, (void*)&CaptureScreen_old);
        if (!CaptureScreen_orig_old) {
          const uint64_t capture5 = Get_Address_of_Method(
              service_capture, capture_namespace.c_str(), capture_controller.c_str(), capture_screen.c_str(), 5);
          if (capture5)
            CaptureScreen_orig_new = (void(*)(MonoObject*, int, long, int, MonoString*, MonoObject*))
                DetourFunction(capture5, (void*)&CaptureScreen_new);
        }
        const uint64_t share_method = Get_Address_of_Method(
            service_capture, capture_namespace.c_str(), event_manager.c_str(), onshare_button.c_str(), 1);
        if (share_method)
          OnShareButton_orig = (void(*)(MonoObject*))DetourFunction(share_method, (void*)&OnShareButton);
      }
      if (service_react_shell && service_string_api) {
        const uint64_t option_method = Get_Address_of_Method(
            service_react_shell, "ReactNative.Modules.ShellUI.HomeUI",
            "OptionMenu", "createJson", 8);
        if (option_method) {
          void *trampoline = DetourFunction(option_method, (void*)&createJson_hook);
          if (trampoline)
            createJson = (void(*)(MonoObject*, MonoObject*, MonoString*, MonoString*,
                                  MonoString*, MonoString*, MonoString*, MonoObject*, bool))trampoline;
        }
      }

      // R7.6: native game Options -> PIZZA HEN Cheats. These are not new
      // hooks: they are the exact Legacy/BootHelper/manifest handlers already
      // used by the full etaHEN-derived ShellUI path below. The only change is
      // ownership: the lazy service installs them on demand after Toolbox open,
      // never immediately after KStuff selection.
      MonoImage *service_legacy = getDLLimage(legacy_dec.c_str());
      MonoImage *service_mscorlib = getDLLimage(mscorlib_dll.c_str());
      if (!service_legacy || !service_mscorlib) {
        shellui_log("PIZZA HEN R7.6: native Cheats missing Legacy/mscorlib image");
        unlink(PIZZAHEN_SHELL_SERVICE_ONLINE);
        set_proc_authid(pid, old_authid);
        return -1;
      }

      const uint64_t service_onpress = Get_Address_of_Method(
          service_legacy, UI3_dec.c_str(), SettingsPage_dec.c_str(),
          onpressed_method.c_str(), 2);
      if (service_onpress)
        oOnPress = (int(*)(MonoObject*, MonoObject*, MonoObject*))
            DetourFunction(service_onpress, (void*)&OnPress_Hook);

      const uint64_t service_boot3 = Get_Address_of_Method(
          AppSystem_img, appsystem_namespace.c_str(), boot_helper.c_str(),
          boot_method.c_str(), 3);
      if (service_boot3)
        boot_orig = (bool(*)(MonoString*, int, MonoString*))
            DetourFunction(service_boot3, (void*)&uri_boot_hook);
      if (!boot_orig) {
        const uint64_t service_boot2 = Get_Address_of_Method(
            AppSystem_img, appsystem_namespace.c_str(), boot_helper.c_str(),
            boot_method.c_str(), 2);
        if (service_boot2)
          boot_orig_2 = (bool(*)(MonoString*, int))
              DetourFunction(service_boot2, (void*)&uri_boot_hook_2);
      }

      const uint64_t service_oncreating = Get_Address_of_Method(
          service_legacy, UI3_dec.c_str(), SettingsPage_dec.c_str(),
          oncreating_method.c_str(), 1);
      if (service_oncreating)
        oOnPreCreate = (int(*)(MonoObject*, MonoObject*))
            DetourFunction(service_oncreating, (void*)&OnPreCreate_Hook);

      const uint64_t service_manifest = Get_Address_of_Method(
          service_mscorlib, sys_reflection_dec.c_str(),
          is_3xx ? "Assembly" : RuntimeAssembly_dec.c_str(),
          GetManifestResourceStream_dec.c_str(), 1);
      if (service_manifest)
        GetManifestResourceStream_Original = (uint64_t(*)(uint64_t, MonoString*))
            DetourFunction(service_manifest, (void*)&GetManifestResourceStream_Hook);

      if (!oOnPress || (!boot_orig && !boot_orig_2) || !oOnPreCreate ||
          !GetManifestResourceStream_Original) {
        shellui_log("PIZZA HEN R7.6: native Cheats hook chain incomplete");
        unlink(PIZZAHEN_SHELL_SERVICE_ONLINE);
        set_proc_authid(pid, old_authid);
        return -1;
      }

      if (service_react_pui) {
        const uint64_t nav_addr = Get_Address_of_Method(
            service_react_pui, "ReactNative.Views.UI3.View",
            "ReactNavigatorManager", "UpdateNavigationState", 1);
        if (nav_addr)
          ReactNavigatorManager_UpdateNavigationState_Orig =
              (void(*)(MonoObject*, MonoObject*))DetourFunction(
                  nav_addr, (void*)&ReactNavigatorManager_UpdateNavigationState_Hook);
      }
      if (service_react_shell) {
        const uint64_t getmodel_addr = Get_Address_of_Method(
            service_react_shell, "ReactNative.Modules.ShellUI.Settings",
            "DebugSettingsModule", "GetModel", 2);
        if (getmodel_addr)
          DebugSettings_GetModel_Orig =
              (void(*)(MonoObject*, MonoObject*, MonoObject*))DetourFunction(
                  getmodel_addr, (void*)&DebugSettings_GetModel_Hook);
      }

      if (read && !read_orig)
        read_orig = (ssize_t(*)(int, void*, size_t))DetourFunction((uintptr_t)read, (void*)&read_hook);

      if (if_exists("/system_tmp/kstuff_paused")) {
        pause_resume_kstuff(NOT_PAUSED, false);
        unlink("/system_tmp/kstuff_paused");
      }
      set_proc_authid(pid, old_authid);
      FILE *service_pid = fopen(PIZZAHEN_SHELL_SERVICE_PID, "w");
      if (service_pid) { fprintf(service_pid, "%d\n", pid); fflush(service_pid); fsync(fileno(service_pid)); fclose(service_pid); }
      g_pizzahen_service_bigapp_id = sceSystemServiceGetAppIdOfRunningBigApp ?
          sceSystemServiceGetAppIdOfRunningBigApp() : -1;
      shellui_hooks_publish_ready();
      hooked = true;
      touch_file(PIZZAHEN_SHELL_SERVICE_ONLINE);
      touch_file("/system_tmp/toolbox_online");
      unlink("/system_tmp/pizzahen_shell_service_mode");
      shellui_log("PIZZA HEN R7.5.3: source-grounded Shell service ONLINE");
      while (true) sleep(0x100000);
    }

    const char *enc_ver = "\x30\x44\x0d\x1c\x13\x08\x69\x35\x3d\x44\x0d\x46";
    std::vector<unsigned char> dev_ver_string = encrypt_decrypt((unsigned char *)enc_ver, strlen(enc_ver), key_base64);
    std::string dec_ver = std::string(dev_ver_string.begin(), dev_ver_string.end());
    dec_ver += etaHEN_VERSION;
    std::string final_ver;
#if PUBLIC_TEST == 1
    final_ver = dec_ver + "-PUBLIC_TEST" + " (" + sw.version_str + " )";
#elif PRE_RELEASE == 1
    final_ver = dec_ver + " PRE_RELEASE" + " (" + sw.version_str + " )";
#else
    final_ver = dec_ver + " (" + sw.version_str + " )";
#endif
    shellui_log("Decrypted Version: %s", final_ver.c_str());

    if (!SetVersionString(final_ver.c_str())) {
      shellui_log("Failed to set func556");
      return -1;
    }

    int size = ((uint64_t)&toolbox_end - (uint64_t)&toolbox_start);
    int lite_size = ((uint64_t)&toolbox_lite_end - (uint64_t)&toolbox_lite_start);
    std::vector<unsigned char> decrypted_data = encrypt_decrypt(toolbox_start, size, key_base64);
    // Convert decrypted data to a string
    dec_xml_str = std::string(decrypted_data.begin(), decrypted_data.end());
    decrypted_data = encrypt_decrypt(toolbox_lite_start, lite_size, key_base64);
    dec_list_xml_str = std::string(decrypted_data.begin(), decrypted_data.end());
    // Load the assembly    
    std::string PowerManager = base64_decode("UG93ZXJNYW5hZ2Vy");
    std::string term = base64_decode("VGVybWluYXRl");

    MonoImage * leg_img = getDLLimage(legacy_dec.c_str());
    if (!leg_img) {
      notify("Failed to get legacy image");
      return -1;
    }

    MonoImage * mscorelib_image = getDLLimage(mscorlib_dll.c_str());
    if (!mscorelib_image) {
      notify("Failed to get mscorelib image");
      return -1;
    }

    MonoImage * REACTPUI_img = getDLLimage(reactpui_dll.c_str());
    if (!REACTPUI_img) {
      notify("Failed to get image 0.");
      return -1;
    }

    MonoImage * AppSystem_img = getDLLimage(appsystem_dll_name.c_str());
    if (!AppSystem_img) {
      notify("Failed to get image 1.5.");
      return -1;
    }

    MonoImage * image_core = getDLLimage(core_dll.c_str());
    if (!image_core) {
      notify("Failed to get image 1.");
      return -1;
    }

    MonoImage * capture_menu = getDLLimage(capture_menu_dll.c_str());
    if (!capture_menu) {
      notify("Failed to get image 3.");
      return -1;
    }

    MonoImage * lnc_img = getDLLimage("Sce.Vsh.LncUtilWrapper.dll");
    if (!lnc_img) {
      notify("Failed to get image 4.");
     // return -1;
    }

    react_common_img = getDLLimage("ReactNative.Vsh.Common.dll");
    if (!react_common_img) {
      notify("Failed to get image 5.");
      return -1;
    }
    
    MonoImage * ReactNativeShellAppReactNativeShellApp_img = getDLLimage("Sce.Vsh.ShellUI.ReactNativeShellApp.dll");
    if (!ReactNativeShellAppReactNativeShellApp_img) {
      notify("Failed to get image 6.");
      return -1;
    }

    MonoImage* AppInstallUtil_img = getDLLimage("Sce.Vsh.AppInstUtilWrapper.dll");
    if(!AppInstallUtil_img) {
      notify("Failed to get image 7.");
      return -1;
	}

  pui_img = getDLLimage("Sce.PlayStation.PUI.dll");
  if (!pui_img) {
    notify("Failed to get pui image");
    return -1;
  }

  if (1) {
      MonoClass* LayerManager = mono_class_from_name(AppSystem_img, "Sce.Vsh.ShellUI.AppSystem", "LayerManager");
      if (!LayerManager) {
          notify("Failed to get LayerManager class");
          return -1;
      }

      // Get the method - this should return MonoMethod*, not an address
      MonoMethod* FindContainerSceneByPath = mono_class_get_method_from_name(LayerManager, "FindContainerSceneByPath", 1);
      if (!FindContainerSceneByPath) {
          notify("Failed to get FindContainerSceneByPath method");
          return -1;
      }

      // Create the string argument
      MonoString* pathArg = mono_string_new(mono_domain_get(), "Game");

      // Prepare arguments array
      void* args[1];
      args[0] = pathArg;

      // Invoke the method (static call since Instance is nullptr)
      MonoObject* exception = nullptr;
      Game = mono_runtime_invoke(FindContainerSceneByPath, nullptr, args, &exception);
      if (exception) {
          notify("Exception occurred while calling FindContainerSceneByPath");
          return -1;
      }
      if (!Game) {
          notify("Failed to get Game ContainerScene");
          return -1;
      }

      shellui_log("Game ContainerScene: %p", Game);
  }

  // System.Reflection.RuntimeAssembly.GetManifestResourceStream
  uint64_t method = Get_Address_of_Method(mscorelib_image, sys_reflection_dec.c_str(), is_3xx ? "Assembly" : RuntimeAssembly_dec.c_str(), GetManifestResourceStream_dec.c_str(), 1);
  if (!method) {
    notify("Failed to get master address");
    return -1;
  }

  shellui_log("Starting hooking...");
  if (if_exists("/system_tmp/kstuff_paused")) {
    shellui_log("Kstuff Paused, resuming kstuff");
    pause_resume_kstuff(NOT_PAUSED, false);
    unlink("/system_tmp/kstuff_paused");

    while(sceKernelMprotect(&buz, sizeof(buz), PROT_READ | PROT_WRITE | PROT_EXEC) != 0) {
        klog_puts("sceKernelMprotect failed, retrying...");
        sleep(1);
    }
  }

  has_hv_bypass = (sceKernelMprotect( & buz[0], 100, 0x7) == 0);

  Patch_Main_thread_Check(image_core);

  
  OnRender_orig = (void(*)(MonoObject*)) DetourFunction(Get_Address_of_Method(pui_img, "Sce.PlayStation.PUI", "Application", "Update", 0), (void*)&OnRender_Hook);

#if 0
    Orig_AppInstUtilInstallByPackage = (int (*)(MonoString * uri, MonoString * ex_uri, MonoString * playgo_scenario_id, MonoString * content_id, MonoString * content_name, MonoString * icon_url, uint32_t slot, bool is_playgo_enabled, MonoObject * pkg_info, MonoArray * languages, MonoArray * playgo_scenario_ids, MonoArray * content_ids)) DetourFunction(Get_Address_of_Method(AppInstallUtil_img, "Sce.Vsh", "AppInstUtilWrapper", "_AppInstUtilInstallByPackage", 12), (void*)&AppInstUtilInstallByPackage_Hook);
	if (!Orig_AppInstUtilInstallByPackage) {
		notify("Failed to hook AppInstUtilInstallByPackage");
		return -1;
	}

	sceAppInstUtilInstallByPackage_orig = (int (*)(MetaInfo * arg1, SceAppInstallPkgInfo * pkg_info, PlayGoInfo * arg2)) DetourFunction((uintptr_t)sceAppInstUtilInstallByPackage, (void*)&sceAppInstUtilInstallByPackage_hook);
    if (!sceAppInstUtilInstallByPackage_orig) {
        notify("Failed to detour sceAppInstUtilInstallByPackage");
        return -1;
    }
#endif
    if(sceRegMgrGetInt) {
      sceRegMgrGetInt = (int( * )(long, int * )) DetourFunction((uintptr_t)sceRegMgrGetInt, (void *)&sceRegMgrGetInt_hook);
      if (!sceRegMgrGetInt) {
        notify("Failed to detour int func");
        return -1;
      }
    }
    else{
      notify("Failed to find sceRegMgrGetInt");
      return -1;
	}

#if 1
	read_orig = (ssize_t(*)(int fd, void *buf, size_t count)) DetourFunction((uintptr_t)read, (void*)&read_hook);
    if (!read_orig) {
      notify("Failed to detour read func");
      return -1;
	}
#endif

    // R7.5.3: the lazy Shell service owns OptionMenu/createJson.
    // Debug Services keeps its v0.1 path but must not stack this detour.
    bool game_options_service_current = false;
    if (if_exists("/system_tmp/pizzahen_shell_service_online")) {
      FILE *service_pid = fopen("/system_tmp/pizzahen_shell_service_pid", "r");
      int service_pid_value = -1;
      if (service_pid) {
        if (fscanf(service_pid, "%d", &service_pid_value) != 1) service_pid_value = -1;
        fclose(service_pid);
      }
      game_options_service_current = (service_pid_value == pid);
    }
    if (!game_options_service_current) {
      void* createJson_addr = DetourFunction(
          Get_Address_of_Method(ReactNativeShellAppReactNativeShellApp_img,
                                "ReactNative.Modules.ShellUI.HomeUI",
                                "OptionMenu", "createJson", 8),
          (void*)&createJson_hook);
      createJson = (void(*)(MonoObject*, MonoObject*, MonoString*, MonoString*,
                            MonoString*, MonoString*, MonoString*, MonoObject*, bool))
                       createJson_addr;
      if (!createJson_addr) {
        shellui_log("Failed to detour Func Set -3");
        return -1;
      }
    } else {
      shellui_log("PIZZA HEN R7.3: createJson already owned by resident Game Options service");
    }

    LaunchApp_orig = (int( * )(MonoString * , uint64_t * , int, LaunchAppParam * )) DetourFunction(Get_Address_of_Method(lnc_img, "Sce.Vsh.LncUtil", "LncUtilWrapper", "LaunchApp", 4), (void * )&LaunchApp);
    if (!LaunchApp_orig) {
      shellui_log("Failed to detour Func Set -2");
     // return -1;
    }

    void* KillAppWithReason_orig = DetourFunction(Get_Address_of_Method(lnc_img, "Sce.Vsh.LncUtil", "LncUtilWrapper","KillAppWithReason", 2), (void *)&KillAppWithReason_Hook);
    if (!KillAppWithReason_orig) {
      notify("Failed to detour KillAppWithReason");
    }

    UpdateImposeStatusFlag_Orig = (void( * )(MonoObject * , MonoObject * )) DetourFunction(Get_Address_of_Method(AppSystem_img, appsystem_namespace.c_str(), layer_manager.c_str(), update_impose_flag.c_str(), 2), (void * )&UpdateImposeStatusFlag_hook);
    if (!UpdateImposeStatusFlag_Orig) {
      notify("Failed to detour Func Set -1");
    }

    GetData = (GamePadData( * )(int)) DetourFunction(Get_Address_of_Method(image_core, input_namespace.c_str(), gamepad_class.c_str(), getdata_method.c_str(), 1), (void * )&GetData_hook);
    if (!GetData) {
      notify("Failed to detour Func Set0");
      return -1;
    }

    CxmlUri = (MonoString * ( * )(MonoObject * , MonoString * )) DetourFunction(Get_Address_of_Method(leg_img, UI3_dec.c_str(), SettingsPlugin_dec.c_str(), cxml_dec.c_str(), 1), (void * )&CxmlUri_Hook);
    if (!CxmlUri) {
      notify("Failed to detour Func Set1");
    }

#if 1
    CallDecrypt_orig = (void( * )(unsigned char * , int, int, int * , int * )) DetourFunction(Get_Address_of_Method(REACTPUI_img, security_namespace.c_str(), bundle_decryptor.c_str(), decrypt_method.c_str(), 5), (void * )&CallDecrypt);
    if (!CallDecrypt_orig) {
      if (ioctl) {
         shellui_log("Found ioctl at %p", ioctl);
         DetourFunction((uintptr_t)ioctl, (void *)&ioctl_hook);
         shellui_log("Detoured ioctl to ioctl_Hook");
       } else {
         notify("Failed to find func workaround");
         return -1;
       }
    }
#endif
    if (!game_options_service_current) {
      oOnPress = (int( * )(MonoObject * , MonoObject * , MonoObject * )) DetourFunction(Get_Address_of_Method(leg_img, UI3_dec.c_str(), SettingsPage_dec.c_str(), onpressed_method.c_str(), 2), (void * )&OnPress_Hook);
      if (!oOnPress) {
        shellui_log("Failed to detour Func Set3");
      }

      boot_orig = (bool( * )(MonoString * , int, MonoString * )) DetourFunction(Get_Address_of_Method(AppSystem_img, appsystem_namespace.c_str(), boot_helper.c_str(), boot_method.c_str(), 3), (void * )&uri_boot_hook);
      if (!boot_orig) {
        boot_orig_2 = (bool( * )(MonoString * , int)) DetourFunction(Get_Address_of_Method(AppSystem_img, appsystem_namespace.c_str(), boot_helper.c_str(), boot_method.c_str(), 2), (void * )&uri_boot_hook_2);
        if (!boot_orig_2) {
          notify("failed to detour Func Set4");
        }
      }
    } else {
      shellui_log("PIZZA HEN R7.6: native Cheats OnPress/Boot already owned by lazy Shell service");
    }

    // OnionHEN 0.0.10: Settings-internal navigation can bypass BootHelper on
    // 11.6+/12.x. These two hooks are optional but together prevent Sony's
    // RN DebugSettingsScreen from becoming the host for PIZZA Debug Services.
    {
      const uint64_t nav_addr = Get_Address_of_Method(
          REACTPUI_img, "ReactNative.Views.UI3.View",
          "ReactNavigatorManager", "UpdateNavigationState", 1);
      if (nav_addr) {
        ReactNavigatorManager_UpdateNavigationState_Orig =
            (void(*)(MonoObject*, MonoObject*))DetourFunction(
                nav_addr, (void*)&ReactNavigatorManager_UpdateNavigationState_Hook);
        shellui_log("PIZZA HEN Onion nav UpdateNavigationState hook: %s",
                    ReactNavigatorManager_UpdateNavigationState_Orig ? "ready" : "detour-failed");
      } else {
        shellui_log("PIZZA HEN Onion nav UpdateNavigationState: method unavailable");
      }

      const uint64_t getmodel_addr = Get_Address_of_Method(
          ReactNativeShellAppReactNativeShellApp_img,
          "ReactNative.Modules.ShellUI.Settings",
          "DebugSettingsModule", "GetModel", 2);
      if (getmodel_addr) {
        DebugSettings_GetModel_Orig =
            (void(*)(MonoObject*, MonoObject*, MonoObject*))DetourFunction(
                getmodel_addr, (void*)&DebugSettings_GetModel_Hook);
        shellui_log("PIZZA HEN Onion nav DebugSettings.GetModel hook: %s",
                    DebugSettings_GetModel_Orig ? "ready" : "detour-failed");
      } else {
        shellui_log("PIZZA HEN Onion nav DebugSettings.GetModel: method unavailable");
      }
    }

    CaptureScreen_orig_old = (void( * )(MonoObject *, int, long, int, MonoObject * )) DetourFunction(Get_Address_of_Method(capture_menu, capture_namespace.c_str(), capture_controller.c_str(), capture_screen.c_str(), 4), (void * )&CaptureScreen_old);
    if (!CaptureScreen_orig_old) {
        CaptureScreen_orig_new = (void( * )(MonoObject *, int, long, int, MonoString * , MonoObject * )) DetourFunction(Get_Address_of_Method(capture_menu, capture_namespace.c_str(), capture_controller.c_str(), capture_screen.c_str(), 5), (void * )&CaptureScreen_new);
        if(!CaptureScreen_orig_new) {
           notify("Failed to detour Func Set5");
        }
    }

    OnShareButton_orig = (void( * )(MonoObject * )) DetourFunction(Get_Address_of_Method(capture_menu, capture_namespace.c_str(), event_manager.c_str(), onshare_button.c_str(), 1), (void * )&OnShareButton);
    if (!OnShareButton_orig) {
      notify("Failed to detour Func Set6");
    }

    if (!game_options_service_current) {
      oOnPreCreate = (int( * )(MonoObject * , MonoObject * )) DetourFunction(Get_Address_of_Method(leg_img, UI3_dec.c_str(), SettingsPage_dec.c_str(), oncreating_method.c_str(), 1), (void * )&OnPreCreate_Hook);
      if (!oOnPreCreate) {
        notify("Failed to detour Func Set7");
      }
    } else {
      shellui_log("PIZZA HEN R7.6: native Cheats OnCreating already owned by lazy Shell service");
    }

    oGetString = (MonoString * ( * )(MonoObject * , MonoString * )) DetourFunction(Get_Address_of_Method(leg_img, UI3_dec.c_str(), SettingsPlugin_dec.c_str(), getstring_method.c_str(), 1), (void * )&GetString_Hook);
    if (!oGetString) {
      notify("Failed to detour Func Set8");
      return -1;
    }

    if (!game_options_service_current) {
      GetManifestResourceStream_Original = (uint64_t( * )(uint64_t, MonoString * ))(DetourFunction(method, (void * ) & GetManifestResourceStream_Hook));
      if (!GetManifestResourceStream_Original) {
        notify("Failed to detour Func Set9");
      }
    } else {
      shellui_log("PIZZA HEN R7.6: native Cheats manifest hook already owned by lazy Shell service");
    }

    shellui_log("Performing Magic ....");
    // rest mode without a network
    oTerminate = (void( * )(void))(DetourFunction(Get_Address_of_Method(AppSystem_img, appsystem_namespace.c_str(), PowerManager.c_str(), term.c_str(), 0), (void * )&Terminate));
    if (!oTerminate) {
      notify("Failed to detour Func Set 10");
    }

    IPC_Client & main_ipc = IPC_Client::getInstance(false);
    is_testkit = main_ipc.IsTestKit();
    if (is_testkit) {
      shellui_log("TestKit Detected, applying shellui testkit hooks");
      Start_Kit_Hooks();
    }
#if 0
    Orig_ReloadApp = (void(*)(MonoString*))DetourFunction(Get_Address_of_Method(react_common_img, "ReactNative.Vsh.Common", "ReactApplicationSceneManager", "ReloadApp", 1), (void * )&ReloadApp);
    if (!Orig_ReloadApp) {
      notify("Failed to detour Func Set 11");
    }
#endif
    //
    // Restore normal authid
    //
    set_proc_authid(pid, old_authid);
    //
    // Continue
    //
    if(global_conf.display_tids)
       ReloadRNPSApp("NPXS40002"); // home screen tid


    // shellui_log("Decrypted Data: %s", dec_xml_str.c_str());
    shellui_log("Performed Magic");

    shellui_hooks_publish_ready();
    hooked = true;
    pthread_t thread_id;
    scePthreadCreate(&thread_id, nullptr, dialogue_thread, nullptr, "dialogue_thread");

    // file to let the main daemon know that its finished loading
    touch_file("/system_tmp/toolbox_online");

    while (true) {
      shellui_log("sleeping ....");
      sleep(0x100000);
    }
    return 0;
    }
}
