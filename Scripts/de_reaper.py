#!/usr/bin/env python3
import sys
import time
import subprocess
from art import AsciiArt
from utils import Colors, clear_screen, print_color, loading_bar, get_input, run_command

def draw_splash():
    clear_screen()
    print_color(AsciiArt.DE_REAPER_SPLASH, Colors.BRRED)

    print_color("     [ PROTOCOL: DESKTOP EXECUTION ] [ TARGET: BLOATWARE ]", Colors.BRBLACK)
    print()

    print_color("  > INITIALIZING KILL CHAIN ", Colors.BRCYAN, end='')
    loading_bar(5, 0.05, '█', '', '')
    loading_bar(5, 0.05, '▒', '', ' [ARMED]')

    print_color("  > SCANNING PACKAGE DATABASE ", Colors.BRCYAN, end='')
    loading_bar(8, 0.03, '▓', '', ' [LOCKED]')
    time.sleep(0.5)

def draw_header():
    clear_screen()
    print_color(AsciiArt.DE_REAPER_HEADER, Colors.BRRED)

def draw_footer():
    print_color("╠══════════════════════════════════════════════════════════════╣", Colors.BRBLACK)
    print_color("║  SYSTEM: Haswell Node  |  USER: DaRipper  |  MODE: NUCLEAR   ║", Colors.BRBLACK)
    print_color("╚══════════════════════════════════════════════════════════════╝", Colors.BRBLACK)

def main():
    draw_splash()
    draw_header()

    # 1. SCAN PHASE
    print()
    print_color("  [ SCANNING SECTOR: PACKAGE GROUPS ]", Colors.BRYELLOW)
    print_color("  ───────────────────────────────────", Colors.BRYELLOW)

    target_groups = [
        "gnome", "gnome-extra", "plasma", "plasma-meta", "plasma-desktop",
        "xfce4", "xfce4-goodies", "mate", "mate-extra", "cinnamon",
        "budgie-desktop", "deepin", "lxqt", "i3-gaps", "sway", "hyprland"
    ]
    found_groups = []

    for group in target_groups:
        # pacman -Qg check
        res = run_command(["pacman", "-Qg", group])
        if res.returncode == 0:
            found_groups.append(group)
            print_color(f"  > DETECTED HOSTILE: {Colors.BRCYAN}{group}", Colors.BRRED)
            time.sleep(0.1)

    if not found_groups:
        print()
        print_color("  > SECTOR CLEAR. NO DESKTOP GROUPS FOUND.", Colors.GREEN)
        return

    print()
    print_color("  [ TACTICAL ANALYSIS ]", Colors.BRGREY)
    print_color("  Multi-Desktop config detected. Select target for IMMEDIATE PURGE.", Colors.BRGREY)
    print_color("  Method: Cascade Removal (-Rcns). Collateral damage expected.", Colors.BRGREY)
    print()

    # 2. MENU PHASE
    for idx, group in enumerate(found_groups, 1):
        print_color(f"  [{idx}] ", Colors.BRRED, end='')
        print_color(group, Colors.WHITE)

    print_color("  [0] ABORT MISSION", Colors.BRBLACK)

    print()
    draw_footer()
    selection = get_input("  AWAITING KILL ORDER >> ", Colors.BRRED)

    if not selection or selection == "0":
        print_color("  > MISSION ABORTED.", Colors.GREEN)
        return

    try:
        idx = int(selection)
        if 1 <= idx <= len(found_groups):
            target = found_groups[idx-1]

            # 3. EXECUTION PHASE
            draw_header()
            print()
            print_color("  ╔════════════════════════════════════╗", Colors.BRRED)
            print_color("  ║      WARNING: CASCADE ENGAGED      ║", Colors.BRRED)
            print_color("  ╚════════════════════════════════════╝", Colors.BRRED)
            print()
            print_color(f"  > TARGET: {target}", Colors.BRYELLOW)
            print_color("  > PROTOCOL: pacman -Rcns", Colors.BRYELLOW)
            print_color("  > STATUS: CALCULATING DEPENDENCY CHAIN...", Colors.BRYELLOW)
            print()

            # The Nuclear Command
            cmd = ["sudo", "pacman", "-Rcns", target]
            subprocess.run(cmd)

            print()
            print_color("  > OPERATION COMPLETE.", Colors.BRCYAN)
            print_color("  > REMINDER: CHECK 'systemctl status display-manager'", Colors.BRCYAN)
        else:
            print_color("  > INVALID TARGET.", Colors.RED)
    except ValueError:
        print_color("  > INVALID TARGET.", Colors.RED)

if __name__ == "__main__":
    main()
