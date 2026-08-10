 __asm__(


    ".global ps5debug_start\n"
	".type   ps5debug_start, @object\n"
	".align  16\n"
	"ps5debug_start:\n"
    	".incbin \"../../../daemon/assets/ps5debug.elf\"\n"
	"ps5debug_end:\n"
	    ".global ps5debug_size\n"
	    ".type   ps5debug_size, @object\n"
	    ".align  4\n"
	"ps5debug_size:\n"
    	".int    ps5debug_end - ps5debug_start\n"


	".global shellui_elf_start\n"
	".type   shellui_elf_start, @object\n"
	".align  16\n"
	"shellui_elf_start:\n"
    	".incbin \"../../../daemon/assets/shellui.elf\"\n"
	"shellui_elf_end:\n"
	    ".global shellui_elf_size\n"
	    ".type   shellui_elf_size, @object\n"
	    ".align  4\n"
	"shellui_elf_size:\n"
    	".int    shellui_elf_end - shellui_elf_start\n"

	".global fps_elf_start\n"
	".type   fps_elf_start, @object\n"
	".align  16\n"
	"fps_elf_start:\n"
    	".incbin \"../../../daemon/assets/fps_elf.elf\"\n"
	"fps_elf_end:\n"
	    ".global fps_elf_size\n"
	    ".type   fps_elf_size, @object\n"
	    ".align  4\n"
	"fps_elf_size:\n"
    	".int    fps_elf_end - fps_elf_start\n"


);

// PIZZA HEN v0.1: the upstream source archive does not ship the app-dumper ELF.
// Keep the ABI symbols but advertise a zero-sized payload so callers can fail safely.
#include <stdint.h>
uint8_t dumper_elf_start[1] = {0};
const unsigned int dumper_elf_size = 0;
