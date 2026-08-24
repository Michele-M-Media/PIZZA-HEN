from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAEMON = ROOT / "Source Code/bootstrapper/source/daemon.c"
s = DAEMON.read_text()
checks = []

def ck(name, cond):
    ok = bool(cond)
    checks.append(ok)
    print(f"{name}=" + ("PASS" if ok else "FAIL"))
    return ok

expected = [
    r'    ".incbin \"../../../bootstrapper/assets/shadowmount_selector.html\"\n"',
    r'    ".incbin \"../../../bin/pizzahen-shadowmount-select.elf\"\n"',
    r'    ".incbin \"../../../bootstrapper/assets/shadowmountplus-experimental.elf\"\n"',
]
for i, line in enumerate(expected, 1):
    ck(f"R7141_INCBIN_{i}_ESCAPED", line in s)

# Catch any C-string .incbin line that contains raw quotes around a path.
bad = []
for lineno, line in enumerate(s.splitlines(), 1):
    if '.incbin ' in line and '.incbin \\"' not in line:
        bad.append((lineno, line))
ck("R7141_NO_RAW_INCBIN_QUOTES", not bad)
if bad:
    for lineno, line in bad:
        print(f"RAW_INCBIN_LINE={lineno}:{line}")

print(f"R7_14_1_INCBIN_COMPILE_REPAIR={sum(checks)}/{len(checks)} " + ("PASS" if all(checks) else "FAIL"))
raise SystemExit(0 if all(checks) else 1)
