#include <stdint.h>
#include <string.h>
#include <sys/types.h>

#include <ps5/kernel.h>

#include "cr_log.h"
#include "jb.h"

#define JB_AUTHID 0x4801000000000013ULL

int
jb_escalate_pid(pid_t pid) {
  if (pid <= 0) {
    return -1;
  }

  if (!kernel_get_proc(pid)) {
    return -1;
  }

  int rc = 0;

  if (kernel_set_ucred_uid(pid, 0) != 0) {
    cr_log("warn", "jb", "kernel_set_ucred_uid failed");
    rc = -1;
  }
  if (kernel_set_ucred_ruid(pid, 0) != 0) {
    cr_log("warn", "jb", "kernel_set_ucred_ruid failed");
    rc = -1;
  }
  if (kernel_set_ucred_svuid(pid, 0) != 0) {
    cr_log("warn", "jb", "kernel_set_ucred_svuid failed");
    rc = -1;
  }
  if (kernel_set_ucred_rgid(pid, 0) != 0) {
    cr_log("warn", "jb", "kernel_set_ucred_rgid failed");
    rc = -1;
  }
  if (kernel_set_ucred_svgid(pid, 0) != 0) {
    cr_log("warn", "jb", "kernel_set_ucred_svgid failed");
    rc = -1;
  }

  intptr_t rootvnode = kernel_get_root_vnode();
  if (rootvnode) {
    if (kernel_set_proc_rootdir(pid, rootvnode) != 0) {
      cr_log("warn", "jb", "kernel_set_proc_rootdir failed");
      rc = -1;
    }
    if (kernel_set_proc_jaildir(pid, rootvnode) != 0) {
      cr_log("warn", "jb", "kernel_set_proc_jaildir failed");
      rc = -1;
    }
  } else {
    cr_log("warn", "jb", "kernel_get_root_vnode returned 0");
    rc = -1;
  }

  if (kernel_set_ucred_authid(pid, JB_AUTHID) != 0) {
    cr_log("warn", "jb", "kernel_set_ucred_authid failed");
    rc = -1;
  }

  uint8_t caps[16];
  memset(caps, 0xff, sizeof(caps));
  if (kernel_set_ucred_caps(pid, caps) != 0) {
    cr_log("warn", "jb", "kernel_set_ucred_caps failed");
    rc = -1;
  }

  return rc;
}
