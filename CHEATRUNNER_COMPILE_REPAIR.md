# CheatRunner integration compile repair

Hardware/WSL build log `PIZZA_HEN_BUILD_20260820-023727.log` reached 79% and failed under `-Werror` in `Source Code/util/source/main.cpp`: the legacy `cheat_cache` pthread handle remained declared after the old PIZZA HEN cheat-cache startup was retired for CheatRunner 0.17.

Repair: remove only the dead `cheat_cache` local variable; preserve `ipc_server` and all CheatRunner/Onion/ShellCore runtime logic. The R7.10 integration gate now also requires that the dead handle is absent.

This is a compile-only cleanup; it does not change CheatRunner 0.17 source, port 9999, Toolbox routing, Debug Services, Onion routing, ShellCore resolver, KStuff selector, or ShadowMount.
