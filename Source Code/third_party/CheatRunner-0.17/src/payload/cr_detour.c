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

Ported from etaHEN's shellui/src/Detour.cpp. Jump uses mov r11,imm64/jmp r11
(FF25 faults on XO pages) via kernel_mprotect (mdbg_copyin fails self-targeted). */

#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <machine/param.h>
#include <sys/mman.h>

#include <ps5/kernel.h>
#include <ps5/klog.h>
#include <ps5/mdbg.h>

#include "cr_detour.h"
#include "hde64.h"

static void
cr_write_jump(uint64_t address, uint64_t destination) {
  *(uint8_t *)(address)     = 0xFF;
  *(uint8_t *)(address + 1) = 0x25;
  *(uint8_t *)(address + 2) = 0x00;
  *(uint8_t *)(address + 3) = 0x00;
  *(uint8_t *)(address + 4) = 0x00;
  *(uint8_t *)(address + 5) = 0x00;
  *(uint64_t *)(address + 6) = destination;
}

/* mov r11,imm64/jmp r11/nop — same 14 bytes as cr_write_jump but reads
 * nothing off the page, so it works on execute-only pages. Clobbers r11. */
static void
cr_build_xo_safe_jump(uint8_t out[CR_HOOK_LENGTH], uint64_t destination) {
  out[0] = 0x49; out[1] = 0xBB;                     /* mov r11, imm64 */
  memcpy(out + 2, &destination, 8);
  out[10] = 0x41; out[11] = 0xFF; out[12] = 0xE3;   /* jmp r11 */
  out[13] = 0x90;                                   /* nop pad */
}

void
cr_write_memory(uint64_t address, void *buffer, int length) {
  memcpy((void *)address, buffer, length);
}

void
cr_patch_in_jump(uint64_t address, void *destination) {
  if (!address || !destination) {
    return;
  }
  cr_write_jump(address, (uint64_t)destination);
}

void *
cr_detour_function(uint64_t address, void *destination) {
  if (!address || !destination) {
    return NULL;
  }

  uint32_t instruction_size = 0;
  pid_t pid = getpid();

  /* read the prologue via mdbg_copyout, not a raw pointer deref */
  uint8_t prologue[32];
  memset(prologue, 0x00, sizeof(prologue));
  if (mdbg_copyout(pid, (intptr_t)address, prologue, sizeof(prologue)) != 0) {
    klog_puts("cr_detour_function: mdbg_copyout of target prologue failed\n");
    return NULL;
  }

  /* mov r11,imm64 is our own jump — if it's already there, this address is
   * already hooked (e.g. an earlier injection); leave it alone. */
  if (prologue[0] == 0x49 && prologue[1] == 0xBB) {
    klog_puts("cr_detour_function: target already hooked, skipping\n");
    return CR_DETOUR_ALREADY_HOOKED;
  }

  while (instruction_size < CR_HOOK_LENGTH) {
    hde64s hs;
    uint32_t insn_len = hde64_disasm(prologue + instruction_size, &hs);

    if (hs.flags & F_ERROR) {
      klog_puts("cr_detour_function: disasm error in target prologue\n");
      return NULL;
    }

    instruction_size += insn_len;
  }

  if (instruction_size > sizeof(prologue) - CR_HOOK_LENGTH) {
    /* would read past the local prologue buffer otherwise */
    klog_printf("cr_detour_function: instruction_size %u too large for prologue buffer\n",
                instruction_size);
    return NULL;
  }

  int stub_length = (int)instruction_size + CR_HOOK_LENGTH;
  void *executable_address = malloc(stub_length);
  if (!executable_address) {
    klog_puts("cr_detour_function: failed to allocate memory for stub\n");
    return NULL;
  }

  if (kernel_mprotect(pid, (uint64_t)executable_address, stub_length,
                       PROT_EXEC | PROT_READ | PROT_WRITE) != 0) {
    klog_puts("cr_detour_function: mprotect on trampoline failed\n");
    free(executable_address);
    return NULL;
  }

  memcpy(executable_address, prologue, instruction_size);
  /* jump back past the stolen bytes; trampoline is our own heap memory,
   * not XO, so the plain FF25 form is fine here */
  cr_patch_in_jump((uint64_t)executable_address + instruction_size,
                    (void *)(address + instruction_size));

  if (kernel_mprotect(pid, address, PAGE_SIZE, PROT_EXEC | PROT_READ | PROT_WRITE) != 0) {
    klog_puts("cr_detour_function: mprotect on target page failed, bailing out\n");
    free(executable_address);
    return NULL;
  }

  uint8_t xo_safe_jump[CR_HOOK_LENGTH];
  cr_build_xo_safe_jump(xo_safe_jump, (uint64_t)destination);
  cr_write_memory(address, xo_safe_jump, CR_HOOK_LENGTH);

  return executable_address;
}
