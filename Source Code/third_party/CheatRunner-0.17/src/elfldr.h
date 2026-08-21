/* Copyright (C) 2024 John Törnblom

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

Adapted for CheatRunner from PS5-Payload-dev/elfldr: trimmed to the
subset used to inject an ELF into an already-running process. The
network-receive (elfldr_read) and spawn-a-new-process (elfldr_spawn) paths
from upstream are not needed here and were removed; use
find_pid_by_name() (cr_game_monitor.h) in place of upstream's
elfldr_find_pid(). */

#pragma once

#include <stdint.h>
#include <sys/types.h>

/**
 * Execute an ELF file in a given process.
 **/
int elfldr_exec(pid_t pid, int stdio, uint8_t* elf);

int elfldr_sanity_check(uint8_t *elf, size_t elf_size);

int elfldr_raise_privileges(pid_t pid);
