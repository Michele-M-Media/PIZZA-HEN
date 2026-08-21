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

Adapted for CheatRunner from PS5-Payload-dev/elfldr (see elfldr.h). Only
elfldr_prepare_exec's entry-point handoff is CheatRunner's own; rest is upstream. */

#include <elf.h>
#include <errno.h>
#include <pthread.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <netinet/in.h>
#include <machine/param.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/wait.h>

#include <ps5/kernel.h>

#include "elfldr.h"
#include "cr_elfldr_log.h"
#include "pt.h"


#ifndef IPV6_2292PKTOPTIONS
#define IPV6_2292PKTOPTIONS 25
#endif


/**
 * Convenient macros.
 **/
#define ROUND_PG(x) (((x) + (PAGE_SIZE - 1)) & ~(PAGE_SIZE - 1))
#define TRUNC_PG(x) ((x) & ~(PAGE_SIZE - 1))
#define PFLAGS(x)   ((((x) & PF_R) ? PROT_READ  : 0) | \
		     (((x) & PF_W) ? PROT_WRITE : 0) | \
		     (((x) & PF_X) ? PROT_EXEC  : 0))

/* scratch stack for the pthread_create stub - must not reuse the hijacked
 * thread's own stack (see elfldr_prepare_exec). */
#define ELFLDR_STUB_STACK_SIZE (16 * 1024)


/**
 * Context structure for the ELF loader.
 **/
typedef struct elfldr_ctx {
  uint8_t* elf;
  pid_t    pid;

  intptr_t base_addr;
  size_t   base_size;
  void*    base_mirror;
} elfldr_ctx_t;


/**
* Parse a R_X86_64_RELATIVE relocatable.
**/
static int
r_relative(elfldr_ctx_t *ctx, Elf64_Rela* rela) {
  intptr_t* loc = ctx->base_mirror + rela->r_offset;
  intptr_t val = ctx->base_addr + rela->r_addend;

  *loc = val;

  return 0;
}


/**
 * Parse a PT_LOAD program header.
 **/
static int
data_load(elfldr_ctx_t *ctx, Elf64_Phdr *phdr) {
  void* data = ctx->base_mirror + phdr->p_vaddr;

  if(!phdr->p_memsz) {
    return 0;
  }

  if(!phdr->p_filesz) {
    return 0;
  }

  memcpy(data, ctx->elf+phdr->p_offset, phdr->p_filesz);

  return 0;
}


int
elfldr_sanity_check(uint8_t *elf, size_t elf_size) {
  Elf64_Ehdr *ehdr = (Elf64_Ehdr*)elf;
  Elf64_Phdr *phdr;

  if(elf_size < sizeof(Elf64_Ehdr) ||
     elf_size < sizeof(Elf64_Phdr) + ehdr->e_phoff ||
     elf_size < sizeof(Elf64_Shdr) + ehdr->e_shoff) {
    return -1;
  }

  if(ehdr->e_ident[0] != 0x7f || ehdr->e_ident[1] != 'E' ||
     ehdr->e_ident[2] != 'L'  || ehdr->e_ident[3] != 'F') {
    return -1;
  }

  phdr = (Elf64_Phdr*)(elf + ehdr->e_phoff);
  for(int i=0; i<ehdr->e_phnum; i++) {
    if(phdr[i].p_offset + phdr[i].p_filesz > elf_size) {
      return -1;
    }
  }

  return 0;
}


/**
 * Load an ELF into the address space of a process with the given pid.
 **/
static intptr_t
elfldr_load(pid_t pid, uint8_t *elf) {
  Elf64_Ehdr *ehdr = (Elf64_Ehdr*)elf;
  Elf64_Phdr *phdr = (Elf64_Phdr*)(elf + ehdr->e_phoff);
  Elf64_Shdr *shdr = (Elf64_Shdr*)(elf + ehdr->e_shoff);

  elfldr_ctx_t ctx = {.elf = elf, .pid=pid};

  size_t min_vaddr = -1;
  size_t max_vaddr = 0;

  int error = 0;

  // Compute size of virtual memory region.
  for(int i=0; i<ehdr->e_phnum; i++) {
    if(phdr[i].p_vaddr < min_vaddr) {
      min_vaddr = phdr[i].p_vaddr;
    }

    if(max_vaddr < phdr[i].p_vaddr + phdr[i].p_memsz) {
      max_vaddr = phdr[i].p_vaddr + phdr[i].p_memsz;
    }
  }

  min_vaddr = TRUNC_PG(min_vaddr);
  max_vaddr = ROUND_PG(max_vaddr);
  ctx.base_size = max_vaddr - min_vaddr;

  int flags = MAP_PRIVATE | MAP_ANONYMOUS;
  int prot = PROT_READ | PROT_WRITE;
  if(ehdr->e_type == ET_DYN) {
    ctx.base_addr = 0;
  } else if(ehdr->e_type == ET_EXEC) {
    ctx.base_addr = min_vaddr;
    flags |= MAP_FIXED;
  } else {
    LOG_PUTS("elfldr_load: ELF type not supported");
    return 0;
  }

  if(!(ctx.base_mirror=malloc(ctx.base_size))) {
    LOG_PERROR("malloc");
    return 0;
  }

  // Reserve an address space of sufficient size.
  if((ctx.base_addr=pt_mmap(pid, ctx.base_addr, ctx.base_size, prot,
			    flags, -1, 0)) == -1) {
    LOG_PT_PERROR(pid, "pt_mmap");
    free(ctx.base_mirror);
    return 0;
  }

  // Parse program headers.
  for(int i=0; i<ehdr->e_phnum && !error; i++) {
    switch(phdr[i].p_type) {
    case PT_LOAD:
      error = data_load(&ctx, &phdr[i]);
      break;
    }
  }

  // Apply relocations.
  for(int i=0; i<ehdr->e_shnum && !error; i++) {
    if(shdr[i].sh_type != SHT_RELA) {
      continue;
    }

    Elf64_Rela* rela = (Elf64_Rela*)(elf + shdr[i].sh_offset);
    for(size_t j=0; j<shdr[i].sh_size/sizeof(Elf64_Rela); j++) {
      switch(rela[j].r_info & 0xffffffffl) {
      case R_X86_64_RELATIVE:
	error = r_relative(&ctx, &rela[j]);
	break;
      }
    }
  }

  if(pt_copyin(ctx.pid, ctx.base_mirror, ctx.base_addr, ctx.base_size)) {
    LOG_PERROR("pt_copyin");
    error = 1;
  }

  // Set protection bits on mapped segments.
  for(int i=0; i<ehdr->e_phnum && !error; i++) {
    if(phdr[i].p_type != PT_LOAD || phdr[i].p_memsz == 0) {
      continue;
    }

    if(phdr[i].p_flags & PF_X) {
      if(kernel_mprotect(pid, ctx.base_addr + phdr[i].p_vaddr,
                         ROUND_PG(phdr[i].p_memsz),
                         PFLAGS(phdr[i].p_flags))) {
	LOG_PERROR("kernel_mprotect");
	error = 1;
      }
    } else {
      if(pt_mprotect(pid, ctx.base_addr + phdr[i].p_vaddr,
		     ROUND_PG(phdr[i].p_memsz),
		     PFLAGS(phdr[i].p_flags))) {
	LOG_PT_PERROR(pid, "pt_mprotect");
	error = 1;
      }
    }
  }

  if(pt_msync(pid, ctx.base_addr, ctx.base_size, MS_SYNC)) {
    LOG_PT_PERROR(pid, "pt_msync");
    error = 1;
  }

  free(ctx.base_mirror);

  if(error) {
    pt_munmap(pid, ctx.base_addr, ctx.base_size);
    return 0;
  }

  return ctx.base_addr + ehdr->e_entry;
}


/**
 * Create payload args in the address space of the process with the given pid.
 **/
static intptr_t
elfldr_payload_args(pid_t pid) {
  int victim_sock;
  int master_sock;
  intptr_t buf;
  int pipe0;
  int pipe1;

  if((buf=pt_mmap(pid, 0, PAGE_SIZE, PROT_READ | PROT_WRITE,
		  MAP_ANONYMOUS | MAP_PRIVATE, -1, 0)) == -1) {
    LOG_PT_PERROR(pid, "pt_mmap");
    return 0;
  }

  if((master_sock=pt_socket(pid, AF_INET6, SOCK_DGRAM, IPPROTO_UDP)) < 0) {
    LOG_PT_PERROR(pid, "pt_socket");
    return 0;
  }

  pt_setint(pid, buf+0x00, 20);
  pt_setint(pid, buf+0x04, IPPROTO_IPV6);
  pt_setint(pid, buf+0x08, IPV6_TCLASS);
  pt_setint(pid, buf+0x0c, 0);
  pt_setint(pid, buf+0x10, 0);
  pt_setint(pid, buf+0x14, 0);
  if(pt_setsockopt(pid, master_sock, IPPROTO_IPV6, IPV6_2292PKTOPTIONS, buf, 24)) {
    LOG_PT_PERROR(pid, "pt_setsockopt");
    return 0;
  }

  if((victim_sock=pt_socket(pid, AF_INET6, SOCK_DGRAM, IPPROTO_UDP)) < 0) {
    LOG_PT_PERROR(pid, "pt_socket");
    return 0;
  }

  pt_setint(pid, buf+0x00, 0);
  pt_setint(pid, buf+0x04, 0);
  pt_setint(pid, buf+0x08, 0);
  pt_setint(pid, buf+0x0c, 0);
  pt_setint(pid, buf+0x10, 0);
  if(pt_setsockopt(pid, victim_sock, IPPROTO_IPV6, IPV6_PKTINFO, buf, 20)) {
    LOG_PT_PERROR(pid, "pt_setsockopt");
    return 0;
  }

  if(kernel_overlap_sockets(pid, master_sock, victim_sock)) {
    LOG_PUTS("kernel_overlap_sockets failed");
    return 0;
  }

  if(pt_pipe(pid, buf)) {
    LOG_PT_PERROR(pid, "pt_pipe");
    return 0;
  }
  pipe0 = pt_getint(pid, buf);
  pipe1 = pt_getint(pid, buf+4);

  intptr_t args       = buf;
  intptr_t rwpipe     = buf + 0x100;
  intptr_t rwpair     = buf + 0x200;
  intptr_t kpipe_addr = kernel_get_proc_file(pid, pipe0);
  intptr_t payloadout = buf + 0x300;
  intptr_t getpid      = pt_resolve(pid, "HoLVWNanBBc");

  pt_setlong(pid, args + 0x00, getpid);
  pt_setlong(pid, args + 0x08, rwpipe);
  pt_setlong(pid, args + 0x10, rwpair);
  pt_setlong(pid, args + 0x18, kpipe_addr);
  pt_setlong(pid, args + 0x20, KERNEL_ADDRESS_DATA_BASE);
  pt_setlong(pid, args + 0x28, payloadout);
  pt_setint(pid, rwpipe + 0, pipe0);
  pt_setint(pid, rwpipe + 4, pipe1);
  pt_setint(pid, rwpair + 0, master_sock);
  pt_setint(pid, rwpair + 4, victim_sock);
  pt_setint(pid, payloadout, 0);

  return args;
}


/**
 * Resolve pthread_create in the target; same dual-handle fallback pt_resolve
 * uses for NIDs, since dlsym takes a plain name instead.
 **/
static intptr_t
elfldr_resolve_pthread_create(pid_t pid) {
  intptr_t addr;

  if((addr=kernel_dynlib_dlsym(pid, 0x1, "pthread_create"))) {
    return addr;
  }
  return kernel_dynlib_dlsym(pid, 0x2001, "pthread_create");
}


/**
 * Shellcode for: pthread_create(thread_out, NULL, entry, args); int3;
 * All operands are hardcoded immediates, so it needs no relocation.
 **/
static int
elfldr_build_pthread_stub(uint8_t *out, size_t out_len, intptr_t pthread_create_addr,
                           intptr_t thread_out, intptr_t entry, intptr_t args) {
  size_t i = 0;
  uint64_t v;

  if(out_len < 47) {
    return -1;
  }

  out[i++] = 0x48; out[i++] = 0xBF;              /* mov rdi, thread_out */
  v = (uint64_t)thread_out; memcpy(out + i, &v, 8); i += 8;

  out[i++] = 0x48; out[i++] = 0x31; out[i++] = 0xF6; /* xor rsi, rsi (attr=NULL) */

  out[i++] = 0x48; out[i++] = 0xBA;              /* mov rdx, entry */
  v = (uint64_t)entry; memcpy(out + i, &v, 8); i += 8;

  out[i++] = 0x48; out[i++] = 0xB9;              /* mov rcx, args */
  v = (uint64_t)args; memcpy(out + i, &v, 8); i += 8;

  out[i++] = 0x49; out[i++] = 0xBB;              /* mov r11, pthread_create */
  v = (uint64_t)pthread_create_addr; memcpy(out + i, &v, 8); i += 8;

  out[i++] = 0x41; out[i++] = 0xFF; out[i++] = 0xD3; /* call r11 */
  out[i++] = 0xCC;                               /* int3 */

  return (int)i;
}


#define ELFLDR_HANG_WATCHDOG_MS 8000

typedef struct {
  pid_t pid;
  volatile int *done;
} elfldr_watchdog_arg_t;

/* Safety net for the pt_* and kernel_mprotect calls below - none have their own
 * timeout, and the target stays ptrace-stopped forever if one blocks. */
static void *
elfldr_hang_watchdog(void *arg) {
  elfldr_watchdog_arg_t *wa = (elfldr_watchdog_arg_t *)arg;
  int waited_ms = 0;
  const int step_ms = 100;

  while (waited_ms < ELFLDR_HANG_WATCHDOG_MS) {
    if (*wa->done) {
      return NULL;
    }
    usleep((useconds_t)step_ms * 1000);
    waited_ms += step_ms;
  }

  if (!*wa->done) {
    cr_log("error", "elfldr",
           "pid=%d: injection sequence didn't finish within %dms - killing it "
           "so it doesn't stay stopped forever", (int)wa->pid, ELFLDR_HANG_WATCHDOG_MS);
    kill(wa->pid, SIGKILL);
  }
  return NULL;
}


/**
 * Runs a hand-built stub via PT_CONTINUE + int3 (not pt_call's single-step,
 * which froze SceShellUI 15+s in pthread_create) and restores full GP+FP state after.
 **/
static int
elfldr_prepare_exec(pid_t pid, uint8_t *elf) {
  intptr_t entry;
  intptr_t args;
  intptr_t pthread_create_addr;
  intptr_t thread_out;
  intptr_t stub_addr;
  intptr_t stub_stack = -1;
  uint8_t stub[64];
  int stub_len;
  struct reg bak_reg;
  struct reg run_reg;
  uint8_t bak_fpregs[PT_FPREGS_SIZE];
  int have_bak_regs = 0;
  int status;
  int error = 0;
  pid_t lwp;
  pid_t target = 0;

  volatile int watchdog_done = 0;
  elfldr_watchdog_arg_t wd_arg = { .pid = pid, .done = &watchdog_done };
  pthread_t watchdog_thr;
  int have_watchdog = 0;

  if(!(entry=elfldr_load(pid, elf))) {
    LOG_PUTS("elfldr_load failed");
    return -1;
  }

  if(!(args=elfldr_payload_args(pid))) {
    LOG_PUTS("elfldr_payload_args failed");
    return -1;
  }

  if(!(pthread_create_addr=elfldr_resolve_pthread_create(pid))) {
    LOG_PUTS("couldn't resolve pthread_create");
    return -1;
  }

  /* pthread_t out-param and stub code share the args page's free tail —
   * elfldr_payload_args only uses up to args+0x300 of its page-sized buffer. */
  thread_out = args + 0x310;
  stub_addr  = args + 0x320;

  if((stub_len=elfldr_build_pthread_stub(stub, sizeof(stub), pthread_create_addr,
                                          thread_out, entry, args)) < 0) {
    LOG_PUTS("elfldr_build_pthread_stub failed");
    return -1;
  }

  /* No per-call timeout below, so the watchdog above guards the whole section.
   * Every exit goes through `out` so it always gets stopped and cleaned up. */
  have_watchdog = (pthread_create(&watchdog_thr, NULL, elfldr_hang_watchdog, &wd_arg) == 0);
  if (!have_watchdog) {
    LOG_PUTS("couldn't start hang watchdog - proceeding without it");
  }

  /* Dedicated stack for the stub - reusing the hijacked thread's live stack
   * risks stomping ABI red-zone data it's still using when it resumes. */
  if((stub_stack=pt_mmap(pid, 0, ELFLDR_STUB_STACK_SIZE, PROT_READ | PROT_WRITE,
                          MAP_ANONYMOUS | MAP_PRIVATE, -1, 0)) == -1) {
    LOG_PT_PERROR(pid, "pt_mmap");
    error = -1;
    goto out;
  }

  /* Fault the page in through the kernel-mediated write path (like every
   * other mmap here) instead of leaving it lazy-backed for raw execution to hit first. */
  if(pt_setint(pid, stub_stack, 0)) {
    LOG_PT_PERROR(pid, "pt_setint");
    error = -1;
    goto out;
  }

  if(kernel_mprotect(pid, args, PAGE_SIZE, PROT_READ | PROT_WRITE | PROT_EXEC)) {
    LOG_PERROR("kernel_mprotect");
    error = -1;
    goto out;
  }

  if(pt_copyin(pid, stub, stub_addr, stub_len)) {
    LOG_PT_PERROR(pid, "pt_copyin");
    error = -1;
    goto out;
  }

  /* Pin every register op below to this LWP - plain pid can drift to a
   * different thread on a busy target. Raw id, no negation (that's EINVAL here). */
  if((lwp=pt_get_lwpid(pid)) == -1) {
    LOG_PT_PERROR(pid, "pt_get_lwpid");
    error = -1;
    goto out;
  }
  target = lwp;

  if(pt_getregs(target, &bak_reg)) {
    LOG_PERROR("pt_getregs");
    error = -1;
    goto out;
  }
  if(pt_getfpregs(target, bak_fpregs)) {
    LOG_PERROR("pt_getfpregs");
    error = -1;
    goto out;
  }
  have_bak_regs = 1;

  run_reg = bak_reg;
  run_reg.r_rip = stub_addr;
  /* 16-byte aligned, as the ABI requires immediately before a call */
  run_reg.r_rsp = (stub_stack + ELFLDR_STUB_STACK_SIZE - 0x100) & ~0xFULL;

  if(pt_setregs(target, &run_reg)) {
    LOG_PERROR("pt_setregs");
    error = -1;
    goto out;
  }

  if(pt_continue(target, 0)) {
    LOG_PERROR("pt_continue");
    error = -1;
  } else {
    /* Bounded wait - a blocking waitpid here previously hung this thread (and
     * SceShellUI's IPC) forever if the stub never reached its breakpoint. */
    int waited_ms = 0;
    const int step_ms = 10;
    const int timeout_ms = 3000;
    pid_t wret = 0;

    while(waited_ms < timeout_ms) {
      wret = waitpid(pid, &status, WNOHANG);
      if(wret != 0) {
        break;
      }
      usleep((useconds_t)step_ms * 1000);
      waited_ms += step_ms;
    }

    if(wret == 0) {
      LOG_PUTS("stub timed out — killing the target to avoid hanging its watchers");
      kill(pid, SIGKILL);
      waitpid(pid, &status, 0);
      error = -1;
    } else if(wret == -1) {
      LOG_PERROR("waitpid");
      error = -1;
    } else if(!WIFSTOPPED(status) || WSTOPSIG(status) != SIGTRAP) {
      LOG_PUTS("stub didn't stop cleanly at its breakpoint");
      error = -1;
    }
  }

out:
  /* Stop the watchdog before anything else - it may already be mid-kill from
   * just before this line, so join it and let that settle first. */
  watchdog_done = 1;
  if (have_watchdog) {
    pthread_join(watchdog_thr, NULL);
  }

  /* Deliberately NOT unmapped - pthread_create returning only means the new
   * thread exists, not that it's finished bootstrapping; freeing this immediately was the real (use-after-free) crash. */

  /* Restore only if we actually captured registers - an early failure before
   * pt_getregs/pt_getfpregs means nothing was touched, so there's nothing to restore. */
  if (have_bak_regs) {
    pt_setregs(target, &bak_reg);
    pt_setfpregs(target, bak_fpregs);
  }

  return error;
}


/**
 * Escape jail and raise privileges.
 **/
int
elfldr_raise_privileges(pid_t pid) {
  static const uint8_t caps[16] = {0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
				   0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff};
  intptr_t vnode;

  if(!(vnode=kernel_get_root_vnode())) {
    return -1;
  }
  if(kernel_set_proc_rootdir(pid, vnode)) {
    return -1;
  }
  if(kernel_set_proc_jaildir(pid, 0)) {
    return -1;
  }
  if(kernel_set_ucred_uid(pid, 0)) {
    return -1;
  }
  if(kernel_set_ucred_caps(pid, caps)) {
    return -1;
  }

  return 0;
}


/**
 * Execute an ELF inside the process with the given pid.
 **/
int
elfldr_exec(pid_t pid, int stdio, uint8_t* elf) {
  uint8_t caps[16];
  intptr_t jaildir;
  intptr_t rootdir;
  uint64_t authid;
  int error = 0;

  // backup privileges
  jaildir = kernel_get_proc_jaildir(pid);
  if(!(rootdir=kernel_get_proc_rootdir(pid))) {
    LOG_PUTS("kernel_get_proc_rootdir failed");
    pt_detach(pid, 0);
    return -1;
  }
  if(kernel_get_ucred_caps(pid, caps)) {
    LOG_PUTS("kernel_get_ucred_caps failed");
    pt_detach(pid, 0);
    return -1;
  }
  if(!(authid=kernel_get_ucred_authid(pid))) {
    LOG_PUTS("kernel_get_ucred_authid failed");
    pt_detach(pid, 0);
    return -1;
  }

  if(elfldr_raise_privileges(pid)) {
    LOG_PUTS("Unable to raise privileges");
    pt_detach(pid, 0);
    return -1;
  }

  if(stdio > 0) {
    stdio = pt_rdup(pid, getpid(), stdio);

    pt_close(pid, STDERR_FILENO);
    pt_close(pid, STDOUT_FILENO);
    pt_close(pid, STDIN_FILENO);

    pt_dup2(pid, stdio, STDIN_FILENO);
    pt_dup2(pid, stdio, STDOUT_FILENO);
    pt_dup2(pid, stdio, STDERR_FILENO);

    pt_close(pid, stdio);
  }

  if(elfldr_prepare_exec(pid, elf)) {
    error = -1;
  }

  // restore privileges
  if(kernel_set_proc_jaildir(pid, jaildir)) {
    LOG_PUTS("kernel_set_proc_jaildir failed");
    error = -1;
  }
  if(kernel_set_proc_rootdir(pid, rootdir)) {
    LOG_PUTS("kernel_set_proc_rootdir failed");
    error = -1;
  }

  if(kernel_set_ucred_caps(pid, caps)) {
    LOG_PUTS("kernel_set_ucred_caps failed");
    error = -1;
  }
  if(kernel_set_ucred_authid(pid, authid)) {
    LOG_PUTS("kernel_set_ucred_authid failed");
    error = -1;
  }

  if(pt_detach(pid, 0)) {
    LOG_PERROR("pt_detach");
    error = -1;
  }

  return error;
}
