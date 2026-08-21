#!/usr/bin/env python3
from pathlib import Path
import hashlib, re

ROOT = Path(__file__).resolve().parents[1]
SC = ROOT / 'Source Code'

shell_policy = SC / 'shellui/include/onion_debug_settings_route_policy.hpp'
daemon_policy = SC / 'daemon/include/onion/debug_settings_route_policy.hpp'
EXPECTED_POLICY_SHA = 'f227e28d3e6ebaf1483d042b2d01a15249a80b03c8997aae1ab1014b46536f1e'
for p in (shell_policy, daemon_policy):
    assert hashlib.sha256(p.read_bytes()).hexdigest() == EXPECTED_POLICY_SHA
policy = shell_policy.read_text()

# Exact Onion boundary and 12.x bundle fingerprints.
assert '0x1006ffff' in policy and '0x11000000' in policy
for x in ('0x4e7bec', '0x4e9028', '0x4e9048', '0x4e8e54'):
    assert x in policy
for h in (
    '0xfc, 0x7c, 0x4f, 0x15', # 12.00/12.02
    '0x75, 0x74, 0x7b, 0xb5', # 12.60
    '0x44, 0x5d, 0xa8, 0xbc', # 12.70
    '0x5d, 0x44, 0x61, 0x85', # 12.20/12.40
): assert h in policy

route = (SC/'shellui/src/debug_services_route.cpp').read_text()
nav = (SC/'shellui/src/debug_services_navigator.cpp').read_text()
prx = (SC/'shellui/src/prx.cpp').read_text()
hooks = (SC/'shellui/src/HookFunctions.cpp').read_text()
daemon = (SC/'daemon/source/main.cpp').read_text()
settings = (SC/'shellui/src/settings_bundle_patch.cpp').read_text()
life_h = (SC/'shellui/include/hook_lifecycle.hpp').read_text()
life_c = (SC/'shellui/src/hook_lifecycle.cpp').read_text()
offsets = (SC/'libhijacker/source/offsets.cpp').read_text()
core = (SC/'util/source/cpp_service.cpp').read_text()

# Runtime route is configured once from actual PS5 firmware and used in all route callers.
assert 'pizzahen_configure_debug_services_route(sw.version)' in prx
assert 'pizzahen_debug_services_uses_old_route' in nav
assert 'pizzahen_rewrite_debug_services_route' in hooks
assert 'ReactNavigatorManager", "UpdateNavigationState", 1' in prx
assert 'DebugSettingsModule", "GetModel", 2' in prx
assert 'ReactNative.PUI.dll' in prx
assert 'Sce.Vsh.ShellUI.ReactNativeShellApp.dll' in prx

# Onion install transaction/lifecycle is no longer omitted.
for token in ('shellui_hooks_begin_install', 'shellui_hooks_publish_ready', 'shellui_hooks_are_ready'):
    assert token in life_h + life_c + prx + hooks + nav
assert 'std::atomic<uint8_t>' in life_c
assert prx.count('shellui_hooks_publish_ready();') >= 2 # resident + full paths
for func in ('uri_boot_hook(', 'uri_boot_hook_2(', 'CxmlUri_Hook(', 'GetManifestResourceStream_Hook(', 'OnPress_Hook(', 'OnPreCreate_Hook('):
    pos = hooks.find(func); assert pos >= 0
    assert 'shellui_hooks_are_ready()' in hooks[pos:pos+800]
for func in ('ReactNavigatorManager_UpdateNavigationState_Hook', 'DebugSettings_GetModel_Hook'):
    pos = nav.find(func); assert pos >= 0
    assert 'shellui_hooks_are_ready()' in nav[pos:pos+700]

# Startup interactive toast must use the same firmware policy, not stock debug_settings.
assert 'DebugSettingsRoutePolicy::for_system_version(sys_ver.version)' in daemon
assert 'debug_route.toolbox_uri(onion::debug_settings_route::UriKind::Simple)' in daemon
# direct hard-coded standard URL is forbidden outside copied policy.
main_without_include = daemon
assert '"actionUrl": "pssettings:play?function=debug_settings"' not in main_without_include

# Exact Onion safe Settings RNPS/Hermes algorithm restored: fingerprint validation,
# equal-length labels, SHA1 footer update and stock icon id preserved.
for token in ('settings_bundle_is_supported', 'kHbcSourceHashOffset', 'kHbcFileLengthOffset',
              'apply_equal_length_patch', 'update_hermes_footer_sha1', 'SHA1Init', 'SHA1Final'):
    assert token in settings
assert "'P', 'I', 'Z', 'Z', 'A', ' ', 'H', 'E', 'N', ' ', 'M'" in settings
assert 'static_assert(sizeof(kLegacyOldLabel) == sizeof(kLegacyNewLabel))' in settings
assert 'static_assert(sizeof(kHermesOldLabel) == sizeof(kHermesNewLabel))' in settings
# icon_setting is used only as a validator; never replaced.
assert 'kLegacyOldIcon' in settings
assert 'kLegacyNewIcon' not in settings

# Exact Onion/kstuff allproc fallback for 11.x/12.x. No invented root/security tables.
for c in ('V1100','V1120','V1140','V1160','V1200','V1202','V1220','V1240','V1260','V1270'):
    assert c in offsets
assert 'return 0x2875D70; // OnionHEN/kstuff: 11.00..11.60' in offsets
assert 'return 0x2885E00; // OnionHEN/kstuff: 12.00..12.70' in offsets
assert 'onion-kstuff-allproc' in offsets
# 11/12 remain intentionally absent from root_vnode/security/QA/utoken fallback functions.
for fn in ('legacy_security_flags', 'legacy_qa_flags', 'legacy_utoken_flags', 'legacy_root_vnode'):
    m = re.search(rf'size_t {fn}\(\) \{{(.*?)\n\}}', offsets, re.S); assert m
    assert 'V1100' not in m.group(1) and 'V1200' not in m.group(1)

# Do not lie about the separate legacy /data ShellCore byte patch: no fabricated 12.x cases.
assert 'shellcore_patch_patterns_supported' in core
support = re.search(r'static bool shellcore_patch_patterns_supported\(.*?\) \{(.*?)\n\}', core, re.S)
assert support
assert 'V1200' not in support.group(1) and 'V1270' not in support.group(1)
assert 'capability-skipped' in core

print('ONION_DEEP_AUDIT_REPAIR=PASS')
print('POLICY_SHA256=' + EXPECTED_POLICY_SHA)
print('ONION_ALLPROC_11X=0x2875D70')
print('ONION_ALLPROC_12X=0x2885E00')
print('LEGACY_SHELLCORE_12X_BYTE_PATCH=NOT_INVENTED')
