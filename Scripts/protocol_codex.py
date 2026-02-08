#!/usr/bin/env python3
import sys
import time
import subprocess
import socket
from art import AsciiArt
from utils import Colors, clear_screen, print_color, get_input

def draw_banner():
    clear_screen()
    print_color(AsciiArt.PROTOCOL_CODEX_BANNER, Colors.BRRED)

    print_color("   [ KNOWLEDGE BASE: ACTIVE ] [ USER: DaRipper ]", Colors.BRGREY)
    print_color("   [ SOURCE: ARCH SYSTEMS DIRECTOR v2.1 ]", Colors.BRGREY)
    print("────────────────────────────────────────────────")

def render_sheet(title):
    print_color(f"   >> ACCESSING: {title}", Colors.BRYELLOW)
    print()

def main():
    while True:
        draw_banner()

        print_color("  [1] PACKAGE MANAGEMENT (Pacman/Yay)", Colors.BRCYAN)
        print_color("      └─> Install, Remove, Orphans, Cache Clean", Colors.BRBLACK)

        print_color("  [2] FISH SHELL SYNTAX", Colors.BRCYAN)
        print_color("      └─> Variables, Loops, Functions (vs Bash)", Colors.BRBLACK)

        print_color("  [3] SYSTEMD & LOGS", Colors.BRCYAN)
        print_color("      └─> Services, Journalctl, Failed Units", Colors.BRBLACK)

        print_color("  [4] PERFORMANCE PROTOCOLS (Haswell)", Colors.BRCYAN)
        print_color("      └─> ZRAM, Makeflags, CachyOS Kernels", Colors.BRBLACK)

        print_color("  [5] GIT & NETWORK", Colors.BRCYAN)
        print_color("      └─> SSH, Ports, Git Config", Colors.BRBLACK)

        print()
        print_color("  [0] ", Colors.BRBLACK, end='')
        print_color("CLOSE CODEX", Colors.WHITE)

        print()
        selection = get_input("  SELECT DOSSIER >> ", Colors.BRRED)

        if selection == "1":
            draw_banner()
            render_sheet("PACKAGE MANAGEMENT (The Bible)")
            print("  UPDATE SYSTEM (Zero-Thought):")
            print("    yay -Syu --noconfirm [cite: 5]")
            print()
            print("  INSTALL (Binary Priority):")
            print("    pacman -S <pkg>          (Official)")
            print("    yay -S <pkg>-bin         (AUR - Prefer Binaries)")
            print()
            print("  CLEANUP (Bloat Removal):")
            print("    pacman -Rns <pkg>        (Remove + Configs + Deps)")
            print("    pacman -Qdtq | pacman -Rns - (Kill Orphans)")
            print("    yay -Yc                  (Clean AUR Dependencies)")
            print()
            print("  QUERY:")
            print("    pacman -Qe               (List Explicit Installs) [cite: 13]")
            print("    pacman -Qi <pkg>         (Info & Verification)")
            print("    pactree <pkg>            (View Dependency Tree)")

        elif selection == "2":
            draw_banner()
            render_sheet("FISH SHELL SYNTAX (Compliance)")
            print("  VARIABLES:")
            print("    set -x VAR value         (Global Export - NOT export VAR=val) ")
            print("    set -e VAR               (Erase Variable)")
            print()
            print("  PATH MANIPULATION:")
            print("    fish_add_path /opt/bin   (Permanent Addition)")
            print()
            print("  ALIASES (Functions):")
            print("    alias name='command'")
            print("    funcsave name            (Make Permanent)")
            print()
            print("  LOGIC:")
            print("    if test -f file.txt      (File Exists Check)")
            print("    for i in (seq 1 5); ...; end")

        elif selection == "3":
            draw_banner()
            render_sheet("SYSTEM CONTROL (Systemd)")
            print("  SERVICES:")
            print("    systemctl enable --now <unit>  (Start & Auto-Boot)")
            print("    systemctl disable --now <unit> (Kill & Remove)")
            print("    systemctl list-units --failed  (Find Broken Services)")
            print()
            print("  LOGS (Journalctl):")
            print("    journalctl -p 3 -xb      (Errors only, current boot)")
            print("    journalctl -f            (Follow live logs)")
            print("    journalctl --vacuum-time=2weeks (Clean old logs)")

        elif selection == "4":
            draw_banner()
            render_sheet("HASWELL OPTIMIZATION (CachyOS/Garuda)")
            print("  COMPILATION:")
            print("    MAKEFLAGS=\"-j4\"        (Saturate 4 Threads) ")
            print()
            print("  MEMORY (ZRAM):")
            print("    zram-generator           (Config: /etc/systemd/zram-generator.conf)")
            print("    Ratio: 1.5:1             (12GB Effective on 8GB Stick) ")
            print("    Algo: zstd               (Fast Decompression)")
            print()
            print("  KERNEL:")
            print("    linux-cachyos            (Sched: EEVDF/BORE) ")
            print("    sysctl vm.swappiness=133 (Prefer ZRAM) ")

        elif selection == "5":
            draw_banner()
            render_sheet("NETWORK & UTILITIES")
            print("  GIT:")
            print("    git config --global user.name \"DaRipper\"")
            print("    git commit -am \"fix: message\"")
            print()
            print("  NETWORK:")
            print("    ip -c a                  (Show Colorized IP)")
            print("    ss -tulpn                (Show Listening Ports)")
            print("    nmcli dev wifi list      (Scan Networks)")

        elif selection == "0":
            clear_screen()
            break

        else:
            print_color("  INVALID SELECTION.", Colors.RED)
            time.sleep(0.5)
            continue

        if selection != "0":
            print()
            print("────────────────────────────────────────────────")
            get_input("  [PRESS ENTER TO RETURN TO CODEX]", Colors.BRGREY)

if __name__ == "__main__":
    main()
