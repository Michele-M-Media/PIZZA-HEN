#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SC = ROOT / "Source Code"

policy = (SC / "shellui/include/onion_debug_settings_route_policy.hpp").read_text()
route = (SC / "shellui/src/debug_services_route.cpp").read_text()
hooks = (SC / "shellui/src/HookFunctions.cpp").read_text()
nav = (SC / "shellui/src/debug_services_navigator.cpp").read_text()
prx = (SC / "shellui/src/prx.cpp").read_text()
offsets_h = (SC / "include/offsets.hpp").read_text()
offsets_cpp = (SC / "libhijacker/source/offsets.cpp").read_text()
proc = (SC / "include/kernel/proc.hpp").read_text()
core = (SC / "util/source/cpp_service.cpp").read_text()
dbg = (SC / "libhijacker/source/dbg.cpp").read_text()
hijacker = (SC / "libhijacker/source/hijacker.cpp").read_text()
kernel = (SC / "libhijacker/source/kernel.cpp").read_text()

assert '"standard-through-10.6"' in policy
assert '0x1006ffff' in policy
assert '"old-route-11.x-plus"' in policy
assert '0x11000000' in policy
assert 'debug_settings_old' in policy
assert 'pizzahen_rewrite_debug_services_route' in route
assert 'pizzahen_configure_debug_services_route(sw.version)' in prx
assert 'ReactNavigatorManager_UpdateNavigationState_Hook' in nav
assert 'DebugSettings_GetModel_Hook' in nav
assert '"DebugSettingsScreen"' in nav and '"DebugSettingsOldScreen"' in nav
assert 'ReactNavigatorManager_UpdateNavigationState_Orig' in prx
assert 'DebugSettings_GetModel_Orig' in prx

# No direct PIZZA shortcut should bypass the route adapter anymore.
assert 'GoToURI("pssettings:play?mode=settings&function=debug_settings")' not in hooks
assert 'GoToURI("pssettings:play?mode=settings&function=debug_settings")' not in prx

# Hermes/RNPS bundle patching must not grow Sony strings.
patch = re.search(r'void patch_bundle_strings\([^)]*\) \{(.*?)\n\}', hooks, re.S)
assert patch
assert 'replace_all' not in patch.group(1)

# Previous multi-firmware ShellCore resolver is restored: modern SDK runtime
# symbols first, historical table only as fallback; no invented V11/V12 table.
assert 'core_resolver_available' in offsets_h
assert 'using_sdk_runtime' in offsets_h
assert 'KERNEL_ADDRESS_DATA_BASE' in offsets_cpp
assert '__attribute__((weak))' in offsets_cpp
assert 'sdk_runtime_offset' in offsets_cpp
assert 'proc_p_ucred()' in proc and 'proc_p_fd()' in proc and 'proc_p_pid()' in proc
assert 'PID_OFFSET = 0xBC' not in dbg and 'UCRED_OFFSET = 0x40' not in dbg
assert 'kernel_get_ucred_authid' in dbg and 'kernel_set_ucred_authid' in dbg
assert 'offsets::available(root_vnode_offset)' in hijacker
assert 'kernel_get_proc(pid)' in kernel and '__attribute__((weak))' in kernel
assert 'shellcore_patch_patterns_supported' in core
assert 'capability-skipped' in core
assert 'case V1200' not in core and 'case V1270' not in core

print('PASS: Onion Debug Services + runtime ShellCore multi-firmware repair static gate')
