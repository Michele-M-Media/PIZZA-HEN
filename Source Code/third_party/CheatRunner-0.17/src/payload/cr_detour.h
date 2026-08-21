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
<http://www.gnu.org/licenses/>.

Ported to from etaHEN's shellui/src/Detour.cpp. Dropped the
has_hv_bypass/sceKernelMprotect fork; kernel_mprotect is the only path used. */

#pragma once

#include <stdint.h>
#include <sys/types.h>

#define CR_HOOK_LENGTH 14

/* Distinct from NULL - address was already hooked by an earlier session's
 * payload still resident in the target, not a fresh failure. */
#define CR_DETOUR_ALREADY_HOOKED ((void *)(intptr_t)-1)

void  cr_patch_in_jump(uint64_t address, void *destination);
void  cr_write_memory(uint64_t address, void *buffer, int length);

/* Hooks `address` to jump to `destination`. Returns a heap trampoline that
 * runs the stolen bytes then jumps back, NULL on failure, or CR_DETOUR_ALREADY_HOOKED if already hooked. */
void *cr_detour_function(uint64_t address, void *destination);
