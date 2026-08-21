# PIZZA HEN v1.0 — Onion Debug / ShellCore Deep Audit Repair

Baseline: `PIZZA-HEN-v1.0-MULTILANGUAGE.zip`

This checkpoint performs a second, source-grounded audit of the Debug Services path and the 11.x/12.x ShellCore process resolver. The objective is fidelity to the vendored OnionHEN 0.0.10 reference without inventing unsupported firmware offsets or byte patches.

## Confirmed Onion route policy

The Onion route policy is byte-identical in the Onion reference, PIZZA ShellUI and PIZZA daemon.

SHA-256:
`f227e28d3e6ebaf1483d042b2d01a15249a80b03c8997aae1ab1014b46536f1e`

Firmware routing:
- 3.00 through 10.60: `debug_settings`
- 11.00 and later: `debug_settings_old`

This is intentional. The compatibility boundary is 11.00, not 10.20.

On 11.x/12.x the required legacy path is:
`debug_settings_old -> DebugSettingsOldScreen -> Legacy SettingPage -> GetManifestResourceStream -> PIZZA HEN XML`

## Deep-audit corrections

### 1. Onion hook transaction lifecycle restored

Exact Onion files were added:
- `Source Code/shellui/include/hook_lifecycle.hpp`
- `Source Code/shellui/src/hook_lifecycle.cpp`

The ShellUI hook transaction now enters Installing state before detours and publishes Ready only after the route-critical hooks are installed. Route callbacks pass through to the original implementation until Ready.

This closes a race where a Settings/RN callback could execute while only part of the Onion route chain was installed.

### 2. Remaining hard-coded Sony Debug action removed

The daemon startup interactive notification still contained a direct `debug_settings` action URL. It now obtains its action URL from `DebugSettingsRoutePolicy::for_system_version(sys_ver.version)`.

Therefore on 11.x/12.x the notification and the ShellUI routing use the same `debug_settings_old` policy.

A source scan finds no remaining direct `pssettings:...function=debug_settings` caller outside the copied route-policy headers.

### 3. Onion Settings bundle patcher restored

The previous repair had left `patch_bundle_strings()` effectively disabled. The Onion Settings bundle algorithm has now been ported, with only PIZZA branding/include/log adaptations:
- exact firmware/profile validation;
- exact HBC file length + source hash validation;
- equal-length label replacement;
- Hermes footer SHA-1 recalculation;
- stock `icon_setting` preserved.

No global `icon_setting` rewrite is performed.

PIZZA equal-length replacement label: `★PIZZA HEN Menu`.

### 4. Onion internal Settings navigation path preserved

The 11+/12+ chain includes both Onion interception points:
- `ReactNavigatorManager.UpdateNavigationState`
- `DebugSettingsModule.GetModel`

If Sony attempts to enter `DebugSettingsScreen`, PIZZA redirects to the legacy route. `id_debug_settings` from the RN model path is also redirected.

The 750 ms Onion debounce behavior is preserved to prevent duplicate BootHelper navigation.

### 5. Source-grounded 11.x/12.x allproc resolver restored

The libhijacker fallback now contains the exact Onion/kstuff `allproc` values:
- 11.00 / 11.20 / 11.40 / 11.60: `0x2875D70`
- 12.00 / 12.02 / 12.20 / 12.40 / 12.60 / 12.70: `0x2885E00`

These values were independently cross-checked against the supplied `kstuff-lite-1.10` prosper0gdb offset headers.

Resolver diagnostic name for this fallback: `onion-kstuff-allproc`.

### 6. No fabricated 12.x root/security offsets or ShellCore byte patterns

Onion does not provide source-grounded 11/12 values for the legacy PIZZA fallback functions `root_vnode`, security flags, QA flags or utoken flags. No values were invented.

The separate legacy `/data` ShellCore byte-pattern patch still has no verified 12.x pattern in the available sources. `shellcore_patch_patterns_supported()` therefore does not pretend 12.x support and reports `capability-skipped` when appropriate.

This distinction is important:
- ShellCore/process discovery on 11/12 is now source-grounded through `allproc`.
- A legacy 12.x `/data` byte patch is **not** claimed solved without a real source/pattern.

## Static/host validation

PASS:
- `TESTS/test_onion_deep_audit_repair.py`
- `TESTS/test_onion_shellcore_multifw_repair.py`
- `TESTS/test_r4_onion_multifw_ui_cleanup.py`
- `TESTS/test_fix39_multisdk_portability.py` — 12/12
- `TESTS/test_r7_7_v1_multilanguage.py`
- `TESTS/test_r7_6_3_hidden_legacy_toolbox_hosts_restore.py`
- `hook_lifecycle.cpp` host compile with Clang C++20, `-Wall -Wextra -Werror`
- `settings_bundle_patch.cpp` host compile with Clang C++20, `-Wall -Wextra -Werror`

`TESTS/test_pizzahen_source.py` remains 60/64, with the exact same four failures as the untouched MULTILANGUAGE baseline (`DASHBOARD_NOTIFICATION`, `SELECTOR_SUBPROJECT`, `SELECTOR_TWO_CHOICES`, `DIRECT_SELECTOR_HTML`). This audit did not introduce those pre-existing failures.

Deep audit gate output:
```
ONION_DEEP_AUDIT_REPAIR=PASS
POLICY_SHA256=f227e28d3e6ebaf1483d042b2d01a15249a80b03c8997aae1ab1014b46536f1e
ONION_ALLPROC_11X=0x2875D70
ONION_ALLPROC_12X=0x2885E00
LEGACY_SHELLCORE_12X_BYTE_PATCH=NOT_INVENTED
```

## Hardware status

Not claimed PASS by static analysis. The decisive hardware checkpoint on 12.xx is:
1. load PIZZA HEN;
2. open PIZZA HEN Debug Services from its normal launcher path;
3. also test the interactive notification action;
4. confirm that Sony RN Debug Settings does not remain visible and the PIZZA HEN legacy XML surface opens;
5. inspect the runtime firmware/resolver diagnostics.

A PS5 cross-build was not executed in this artifact environment because `PS5_PAYLOAD_SDK` is not configured here.
