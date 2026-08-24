EchoStretch dump_installer reference
====================================
Repository: https://github.com/EchoStretch/dump_installer
Default branch checked: main
README blob SHA observed: ca19811712e8658f9c50c99325726a008160e368

Upstream README describes Homebrew Dump Installer as using KStuff, Websrv payloads and Homebrew Launcher.
It lists /data/homebrew, /mnt/usb#/homebrew and /mnt/ext#/homebrew as supported placement roots.
ShadowMountPlus is not listed as a requirement in that README.

PIZZA HEN R7.18 therefore exposes an explicit ShadowMount selector choice to skip ShadowMountPlus while continuing the normal post-selector pipeline.
