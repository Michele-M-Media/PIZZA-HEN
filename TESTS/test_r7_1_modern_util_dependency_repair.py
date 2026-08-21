#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
h=(ROOT/'Source Code/util/include/common_utils.h').read_text(errors='ignore')
c=(ROOT/'Source Code/util/source/common_utils.c').read_text(errors='ignore')
pm=(ROOT/'Source Code/util/source/PluginManager.cpp').read_text(errors='ignore')
checks={
 'R71_DECL_PATH_HASH':'uint32_t pizzahen_path_hash(const char *path);' in h,
 'R71_DECL_PID_PATH':'void pizzahen_payload_pid_path(const char *path, char *out, size_t out_size);' in h,
 'R71_DECL_PROC_NAME':'void pizzahen_payload_proc_name(const char *path, char *out, size_t out_size);' in h,
 'R71_IMPL_FNV1A':'uint32_t h = 2166136261u;' in c and 'h *= 16777619u;' in c,
 'R71_IMPL_STABLE_PID':'/system_tmp/PZHNE%08X.PID' in c,
 'R71_IMPL_STABLE_PROC':'PZHNE%08X' in c,
 'R71_ELF_PID_PATH':'pizzahen_payload_pid_path(path, pbuf, sizeof(pbuf));' in c,
 'R71_ELF_PROC_NAME':'pizzahen_payload_proc_name(path, procname, sizeof(procname));' in c,
 'R71_ELF_SPAWN_STABLE':'elfldr_spawn("/", STDOUT_FILENO, buf, procname)' in c,
 'R71_PLUGINMANAGER_DEP_RESOLVED':pm.count('pizzahen_payload_pid_path(')==3,
 'R71_PLUGIN_ABI_UNCHANGED':'snprintf(pbuf, sizeof(pbuf), "/system_tmp/%s.PID", header->titleID);' in c,
}
for k,v in checks.items(): print(('PASS ' if v else 'FAIL ')+k)
if not all(checks.values()): raise SystemExit(1)
print('R7_1_MODERN_UTIL_DEPENDENCY_REPAIR=PASS')
