#include "kernel.hpp"
#include "util.hpp"

extern "C" {
	#include <ps5/kernel.h>
size_t	 strnlen(const char *, size_t);
// Weak keeps compatibility with older SDK layouts that do not export the
// modern direct process resolver.
intptr_t kernel_get_proc(pid_t pid) __attribute__((weak));
}

static constexpr size_t BUF_SIZE = 0x10;

String getKernelString(uintptr_t addr) {
	String res{};
	char buf[BUF_SIZE];
	while (true) {
		kernel_copyout(addr + res.length(), buf, sizeof(buf));
		size_t read = strnlen(buf, sizeof(buf));
		res += StringView{buf, read};
		if (read < sizeof(buf)) {
			return res;
		}
	}
}

UniquePtr<KProc> getProc(int pid) {
	if (&kernel_get_proc != nullptr) {
		const intptr_t proc_addr = kernel_get_proc(pid);
		if (proc_addr != 0) {
			return new KProc{static_cast<uintptr_t>(proc_addr)};
		}
	}

	// Compatibility path for older SDK layouts.
	for (auto p : getAllProcs()) {
		if (pid == p->pid()) {
			return p.release();
		}
	}
	return nullptr;
}

bool createReadWriteSockets(const UniquePtr<KProc> &proc, const int *sockets) noexcept {
	// NOLINTBEGIN(cppcoreguidelines-avoid-magic-numbers)
	auto newtbl = proc->getFdTbl();
	auto sock = newtbl.getFileData(sockets[0]);
	if (sock == 0) [[unlikely]] {
		puts("createReadWriteSockets sock == 0");
		return false;
	}
	kwrite<uint32_t>(sock, 0x100);
	auto pcb = kread<uintptr_t>(sock + 0x18);
	if (pcb == 0) [[unlikely]] {
		puts("createReadWriteSockets master pcb == 0");
		return false;
	}
	auto master_inp6_outputopts = kread<uintptr_t>(pcb + 0x120);
	if (master_inp6_outputopts == 0) [[unlikely]] {
		puts("createReadWriteSockets master_inp6_outputopts == 0");
		return false;
	}
	sock = newtbl.getFileData(sockets[1]);
	kwrite<uint32_t>(sock, 0x100);
	pcb = kread<uintptr_t>(sock + 0x18);
	if (pcb == 0) [[unlikely]] {
		puts("createReadWriteSockets victim pcb == 0");
		return false;
	}
	auto victim_inp6_outputopts = kread<uintptr_t>(pcb + 0x120);
	if (victim_inp6_outputopts == 0) [[unlikely]] {
		puts("createReadWriteSockets victim_inp6_outputopts == 0");
		return false;
	}
	kwrite(master_inp6_outputopts + 0x10, victim_inp6_outputopts + 0x10);
	kwrite<uint32_t>(master_inp6_outputopts + 0xc0, 0x13370000);
	return true;
	// NOLINTEND(cppcoreguidelines-avoid-magic-numbers)
}
