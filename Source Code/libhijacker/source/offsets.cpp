/*
 * PIZZA HEN multi-firmware libhijacker resolver.
 *
 * Primary path: use the PS5 Payload SDK runtime-resolved kernel addresses.
 * This keeps one PIZZA-HEN binary independent from a hard-coded firmware
 * switch whenever the selected SDK exposes the modern KERNEL_ADDRESS_* ABI.
 *
 * Compatibility path: retain etaHEN/libhijacker's historical table for older
 * SDK layouts that do not provide those runtime globals. The compatibility
 * table is deliberately a fallback; it must never override SDK runtime data.
 */

extern "C" {
#include <stdint.h>
#include <stddef.h>
#include <sys/types.h>
#include <sys/sysctl.h>
#include <stdio.h>

/*
 * Weak declarations keep the source buildable with older SDK layouts.
 * On modern ps5-payload-dev SDKs the CRT provides and initializes these
 * objects for the running firmware. If an older SDK does not provide one,
 * its address resolves to null and we fall back to the legacy table.
 */
extern const intptr_t KERNEL_ADDRESS_DATA_BASE      __attribute__((weak));
extern const intptr_t KERNEL_ADDRESS_ALLPROC        __attribute__((weak));
extern const intptr_t KERNEL_ADDRESS_SECURITY_FLAGS __attribute__((weak));
extern const intptr_t KERNEL_ADDRESS_QA_FLAGS       __attribute__((weak));
extern const intptr_t KERNEL_ADDRESS_UTOKEN_FLAGS   __attribute__((weak));
extern const intptr_t KERNEL_ADDRESS_ROOTVNODE      __attribute__((weak));
extern const off_t KERNEL_OFFSET_PROC_P_UCRED __attribute__((weak));
extern const off_t KERNEL_OFFSET_PROC_P_FD    __attribute__((weak));
extern const off_t KERNEL_OFFSET_PROC_P_PID   __attribute__((weak));
}

static constexpr uint32_t VERSION_MASK = 0xffff0000;
static constexpr size_t INVALID_OFFSET = static_cast<size_t>(-1);

static constexpr uint32_t V100 = 0x1000000;
static constexpr uint32_t V101 = 0x1010000;
static constexpr uint32_t V102 = 0x1020000;
static constexpr uint32_t V105 = 0x1050000;
static constexpr uint32_t V110 = 0x1100000;
static constexpr uint32_t V111 = 0x1110000;
static constexpr uint32_t V112 = 0x1120000;
static constexpr uint32_t V113 = 0x1130000;
static constexpr uint32_t V114 = 0x1140000;
static constexpr uint32_t V200 = 0x2000000;
static constexpr uint32_t V220 = 0x2200000;
static constexpr uint32_t V225 = 0x2250000;
static constexpr uint32_t V226 = 0x2260000;
static constexpr uint32_t V230 = 0x2300000;
static constexpr uint32_t V250 = 0x2500000;
static constexpr uint32_t V270 = 0x2700000;
static constexpr uint32_t V300 = 0x3000000;
static constexpr uint32_t V310 = 0x3100000;
static constexpr uint32_t V320 = 0x3200000;
static constexpr uint32_t V321 = 0x3210000;
static constexpr uint32_t V400 = 0x4000000;
static constexpr uint32_t V402 = 0x4020000;
static constexpr uint32_t V403 = 0x4030000;
static constexpr uint32_t V450 = 0x4500000;
static constexpr uint32_t V451 = 0x4510000;
static constexpr uint32_t V500 = 0x5000000;
static constexpr uint32_t V502 = 0x5020000;
static constexpr uint32_t V510 = 0x5100000;
static constexpr uint32_t V550 = 0x5500000;
static constexpr uint32_t V600 = 0x6000000;
static constexpr uint32_t V602 = 0x6020000;
static constexpr uint32_t V650 = 0x6500000;
static constexpr uint32_t V700 = 0x7000000;
static constexpr uint32_t V701 = 0x7010000;
static constexpr uint32_t V720 = 0x7200000;
static constexpr uint32_t V740 = 0x7400000;
static constexpr uint32_t V760 = 0x7600000;
static constexpr uint32_t V761 = 0x7610000;
static constexpr uint32_t V800 = 0x8000000;
static constexpr uint32_t V820 = 0x8200000;
static constexpr uint32_t V840 = 0x8400000;
static constexpr uint32_t V860 = 0x8600000;
static constexpr uint32_t V900 = 0x9000000;
static constexpr uint32_t V905 = 0x9050000;
static constexpr uint32_t V920 = 0x9200000;
static constexpr uint32_t V940 = 0x9400000;
static constexpr uint32_t V960 = 0x9600000;
static constexpr uint32_t V1000 = 0x10000000;
static constexpr uint32_t V1001 = 0x10010000;
static constexpr uint32_t V1020 = 0x10200000;
static constexpr uint32_t V1040 = 0x10400000;
static constexpr uint32_t V1060 = 0x10600000;
// OnionHEN 0.0.10 / kstuff-lite prosper0gdb allproc support.
// Onion intentionally leaves 11.x/12.x root_vnode/security/QA/utoken TBD;
// only the source-grounded allproc values are added here.
static constexpr uint32_t V1100 = 0x11000000;
static constexpr uint32_t V1120 = 0x11200000;
static constexpr uint32_t V1140 = 0x11400000;
static constexpr uint32_t V1160 = 0x11600000;
static constexpr uint32_t V1200 = 0x12000000;
static constexpr uint32_t V1202 = 0x12020000;
static constexpr uint32_t V1220 = 0x12200000;
static constexpr uint32_t V1240 = 0x12400000;
static constexpr uint32_t V1260 = 0x12600000;
static constexpr uint32_t V1270 = 0x12700000;

uint32_t getSystemSwVersion() {
    static uint32_t version;
    if (version != 0) [[likely]] {
        return version;
    }
    size_t size = sizeof(version);
    sysctlbyname("kern.sdk_version", &version, &size, nullptr, 0);
    return version;
}

namespace {

intptr_t weak_value(const intptr_t* symbol) {
    return symbol ? *symbol : 0;
}

size_t sdk_runtime_offset(const intptr_t* symbol, const char* label) {
    const intptr_t base = weak_value(&KERNEL_ADDRESS_DATA_BASE);
    const intptr_t absolute = weak_value(symbol);

    if (base == 0 || absolute == 0 || absolute < base) {
        return INVALID_OFFSET;
    }

    const size_t result = static_cast<size_t>(absolute - base);
    (void)label;
    return result;
}

size_t sdk_or_legacy_struct_offset(const off_t* symbol, size_t legacy) {
    if (symbol != nullptr && *symbol >= 0) {
        return static_cast<size_t>(*symbol);
    }
    return legacy;
}

size_t legacy_allproc() {
    switch (getSystemSwVersion() & VERSION_MASK) {
        case V100: case V101: case V102: case V105:
        case V110: case V111: case V112: case V113: case V114:
            return 0x26D1C18;
        case V200: case V220: case V225: case V226: case V230: case V250: case V270:
            return 0x2701C28;
        case V300: case V310: case V320: case V321:
            return 0x276DC58;
        case V400: case V402: case V403: case V450: case V451:
            return 0x27EDCB8;
        case V500: case V502: case V510: case V550:
            return 0x291DD00;
        case V600: case V602: case V650:
            return 0x2869D20;
        case V700: case V701: case V720: case V740: case V760: case V761:
            return 0x2859D50;
        case V800: case V820: case V840: case V860:
            return 0x2875D50;
        case V900: case V905: case V920: case V940: case V960:
            return 0x2755D50;
        case V1000: case V1001: case V1020: case V1040: case V1060:
            return 0x2765D70;
        case V1100: case V1120: case V1140: case V1160:
            return 0x2875D70; // OnionHEN/kstuff: 11.00..11.60
        case V1200: case V1202: case V1220: case V1240: case V1260: case V1270:
            return 0x2885E00; // OnionHEN/kstuff: 12.00..12.70
        default:
            return INVALID_OFFSET;
    }
}

size_t legacy_security_flags() {
    switch (getSystemSwVersion() & VERSION_MASK) {
        case V100: case V101: case V102: case V105:
        case V110: case V111: case V112: case V113: case V114:
            return 0x6241074;
        case V200: case V220: case V225: case V226: case V230: case V250: case V270:
            return 0x63E1274;
        case V300: case V310: case V320: case V321:
            return 0x6466474;
        case V400:
            return 0x6506474;
        case V402: case V403: case V450: case V451:
            return 0x6505474;
        case V500: case V502: case V510: case V550:
            return 0x66466EC;
        case V600: case V602: case V650:
            return 0x65968EC;
        case V700: case V701: case V720: case V740: case V760: case V761:
            return 0x0AC8064;
        case V800: case V820: case V840: case V860:
            return 0x0AC3064;
        case V900:
            return 0x0D72064;
        case V905: case V920: case V940: case V960:
            return 0x0D73064;
        case V1000: case V1001: case V1020: case V1040: case V1060:
            return 0x0D79064;
        default:
            return INVALID_OFFSET;
    }
}

size_t legacy_qa_flags() {
    switch (getSystemSwVersion() & VERSION_MASK) {
        case V100: case V101: case V102: case V105:
        case V110: case V111: case V112: case V113: case V114:
        case V200: case V220: case V225: case V226: case V230: case V250: case V270:
        case V300: case V310: case V320: case V321:
        case V400: case V402: case V403: case V450: case V451:
        case V500: case V502: case V510: case V550:
            return 0x6241098;
        case V600: case V602: case V650:
            return 0x65968EC + 0x24;
        case V700: case V701: case V720: case V740: case V760: case V761:
            return 0x0AC8064 + 0x24;
        case V800: case V820: case V840: case V860:
            return 0x0AC3064 + 0x24;
        case V900:
            return 0x0D72064 + 0x24;
        case V905: case V920: case V940: case V960:
            return 0x0D73064 + 0x24;
        case V1000: case V1001: case V1020: case V1040: case V1060:
            return 0x0D79064 + 0x24;
        default:
            return INVALID_OFFSET;
    }
}

size_t legacy_utoken_flags() {
    switch (getSystemSwVersion() & VERSION_MASK) {
        case V100: case V101: case V102: case V105:
        case V110: case V111: case V112: case V113: case V114:
        case V200: case V220: case V225: case V226: case V230: case V250: case V270:
        case V300: case V310: case V320: case V321:
        case V400: case V402: case V403: case V450: case V451:
        case V500: case V502: case V510: case V550:
            return 0x6646710;
        case V600: case V602: case V650:
            return 0x65968EC + 0x8C;
        case V700: case V701: case V720: case V740: case V760: case V761:
            return 0x0AC8064 + 0x8C;
        case V800: case V820: case V840: case V860:
            return 0x0AC3064 + 0x8C;
        case V900:
            return 0x0D72064 + 0x8C;
        case V905: case V920: case V940: case V960:
            return 0x0D73064 + 0x8C;
        case V1000: case V1001: case V1020: case V1040: case V1060:
            return 0x0D79064 + 0x8C;
        default:
            return INVALID_OFFSET;
    }
}

size_t legacy_root_vnode() {
    switch (getSystemSwVersion() & VERSION_MASK) {
        case V100: case V101: case V102: case V105:
        case V110: case V111: case V112: case V113: case V114:
            return 0x6565540;
        case V200: case V220: case V225: case V226: case V230: case V250: case V270:
            return 0x67134C0;
        case V300: case V310: case V320: case V321:
            return 0x67AB4C0;
        case V400: case V402: case V403: case V450: case V451:
            return 0x66E74C0;
        case V500: case V502: case V510: case V550:
            return 0x6853510;
        case V600: case V602: case V650:
            return 0x679F510;
        case V700: case V701: case V720: case V740: case V760: case V761:
            return 0x30C7510;
        case V800: case V820: case V840: case V860:
            return 0x30FB510;
        case V900: case V905: case V920: case V940: case V960:
            return 0x2FDB510;
        case V1000: case V1001: case V1020: case V1040: case V1060:
            return 0x2FA3510;
        default:
            return INVALID_OFFSET;
    }
}

size_t resolve_or_legacy(const intptr_t* runtime_symbol,
                         size_t (*legacy_resolver)(),
                         const char* label) {
    const size_t runtime = sdk_runtime_offset(runtime_symbol, label);
    if (runtime != INVALID_OFFSET) [[likely]] {
        return runtime;
    }

    const size_t legacy = legacy_resolver();
    if (legacy != INVALID_OFFSET) {
        return legacy;
    }

    printf("PIZZA HEN: %s unavailable for firmware 0x%x (SDK runtime resolver missing)\n",
           label, getSystemSwVersion() & VERSION_MASK);
    return INVALID_OFFSET;
}

} // namespace

namespace offsets {

size_t allproc() {
    return resolve_or_legacy(&KERNEL_ADDRESS_ALLPROC, legacy_allproc, "allproc");
}

size_t security_flags() {
    return resolve_or_legacy(&KERNEL_ADDRESS_SECURITY_FLAGS, legacy_security_flags, "security_flags");
}

size_t qa_flags() {
    return resolve_or_legacy(&KERNEL_ADDRESS_QA_FLAGS, legacy_qa_flags, "qa_flags");
}

size_t utoken_flags() {
    return resolve_or_legacy(&KERNEL_ADDRESS_UTOKEN_FLAGS, legacy_utoken_flags, "utoken_flags");
}

size_t root_vnode() {
    return resolve_or_legacy(&KERNEL_ADDRESS_ROOTVNODE, legacy_root_vnode, "root_vnode");
}

size_t proc_p_ucred() noexcept {
    return sdk_or_legacy_struct_offset(&KERNEL_OFFSET_PROC_P_UCRED, 0x40);
}

size_t proc_p_fd() noexcept {
    return sdk_or_legacy_struct_offset(&KERNEL_OFFSET_PROC_P_FD, 0x48);
}

size_t proc_p_pid() noexcept {
    return sdk_or_legacy_struct_offset(&KERNEL_OFFSET_PROC_P_PID, 0xBC);
}

bool using_sdk_runtime() noexcept {
    const intptr_t base = weak_value(&KERNEL_ADDRESS_DATA_BASE);
    if (base == 0) {
        return false;
    }
    return sdk_runtime_offset(&KERNEL_ADDRESS_ALLPROC, "allproc") != INVALID_OFFSET;
}

bool core_resolver_available() noexcept {
    return allproc() != INVALID_OFFSET;
}

const char* resolver_name() noexcept {
    if (using_sdk_runtime()) {
        return "sdk-runtime";
    }
    if (legacy_allproc() != INVALID_OFFSET) {
        const uint32_t fw = getSystemSwVersion() & VERSION_MASK;
        if (fw >= V1100 && fw <= V1270)
            return "onion-kstuff-allproc";
        return "legacy-table";
    }
    return "unavailable";
}

} // namespace offsets
