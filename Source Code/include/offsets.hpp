#pragma once

extern "C" {
	#include <stddef.h>
}

namespace offsets {

constexpr size_t unavailable = static_cast<size_t>(-1);
inline bool available(size_t value) noexcept { return value != unavailable; }

size_t allproc();
size_t security_flags();
size_t qa_flags();
size_t utoken_flags();
size_t root_vnode();

// Runtime-resolved struct proc field offsets, with the inherited values only
// as old-SDK fallbacks.
size_t proc_p_ucred() noexcept;
size_t proc_p_fd() noexcept;
size_t proc_p_pid() noexcept;

// Multi-firmware resolver state. Modern SDKs resolve the active firmware at
// runtime; the historical table remains only as a compatibility fallback.
bool using_sdk_runtime() noexcept;
bool core_resolver_available() noexcept;
const char* resolver_name() noexcept;

} // offsets
