#!/usr/bin/env python3
import sys
import time
import subprocess
import shutil
import socket
from art import AsciiArt
from utils import Colors, clear_screen, print_color, get_input, run_command, loading_bar

def draw_splash():
    clear_screen()
    print_color(AsciiArt.EXPAC_MASTER_SPLASH, Colors.BRRED)

    print_color("      [ SYSTEM IDENTITY: DaRipper ] [ ARCHITECTURE: HASWELL ]", Colors.BRBLACK)
    print()

    print_color("  > INITIALIZING NEURAL LINK ", Colors.BRCYAN, end='')
    loading_bar(4, 0.05, '█', '', '')
    loading_bar(4, 0.05, '▒', '', ' [ESTABLISHED]')

    print_color("  > DECRYPTING PACMAN DATABASES ", Colors.BRCYAN, end='')
    loading_bar(8, 0.03, '▓', '', ' [UNLOCKED]')

    print_color("  > PROTOCOL: AGGRESSIVE AUDIT", Colors.BRRED)
    time.sleep(0.4)
    print_color("  > WELCOME BACK, DaRipper.", Colors.BRRED)
    time.sleep(0.6)

def draw_header():
    clear_screen()
    print_color(AsciiArt.EXPAC_MASTER_HEADER, Colors.BRRED)

def draw_footer():
    # Use hostname and uname similar to original
    hostname = socket.gethostname()
    kernel = subprocess.getoutput("uname -r")

    print_color("╠══════════════════════════════════════════════════════════════╣", Colors.BRBLACK)
    print_color(f"║  NODE: {hostname:<15}  ::  KERNEL: {kernel:<15}  ::  USER: DaRipper ║", Colors.BRBLACK)
    print_color("╚══════════════════════════════════════════════════════════════╝", Colors.BRBLACK)

def main():
    if not shutil.which("expac"):
        print_color("CRITICAL: 'expac' MISSING.", Colors.RED)
        return

    draw_splash()

    while True:
        draw_header()

        # Menu
        print()
        print_color("  [1] ", Colors.BRRED, end=''); print_color("MATRIX STREAM", Colors.BRCYAN)
        print_color("      └─> RAW FEED: Name, Repo, Dependencies (No Paging)", Colors.BRBLACK)

        print_color("  [2] ", Colors.BRRED, end=''); print_color("BLOAT HUNTER", Colors.BRCYAN)
        print_color("      └─> TOP 50: Largest install targets (Size Sort)", Colors.BRBLACK)

        print_color("  [3] ", Colors.BRRED, end=''); print_color("TIMELINE LOG", Colors.BRCYAN)
        print_color("      └─> HISTORY: Last 20 system modifications", Colors.BRBLACK)

        print_color("  [4] ", Colors.BRRED, end=''); print_color("INTRUDER SCAN (REPO AUDIT)", Colors.BRCYAN)
        print_color("      └─> SECURITY: Detects non-core/AUR binaries", Colors.BRBLACK)

        print_color("  [5] ", Colors.BRRED, end=''); print_color("DEEP DIVE (TARGET INSPECTOR)", Colors.BRCYAN)
        print_color("      └─> FORENSICS: Full metadata extraction", Colors.BRBLACK)

        print()
        print_color("  [0] ", Colors.BRBLACK, end=''); print_color("DISCONNECT", Colors.WHITE)

        print()
        draw_footer()

        selection = get_input("  AWAITING INPUT >> ", Colors.BRRED)
        print("────────────────────────────────────────────────────────────────")

        if selection == "1":
            print_color(">>> STREAMING DEPENDENCY MATRIX...", Colors.BRCYAN)
            # expac -l ', ' '%n|%r|%N|%o' | sort | column -t -s '|'
            # Python equivalent or just shell out. Shelling out is easier for expac.
            # Header needs to be prepended.

            cmd = "expac -l ', ' '%n|%r|%N|%o' | sort"
            try:
                output = subprocess.check_output(cmd, shell=True, text=True)
                header = "PACKAGE|REPO|DEPENDENTS|OPTIONAL DEPS\n"
                full_output = header + output

                # column -t -s '|'
                p = subprocess.Popen(["column", "-t", "-s", "|"], stdin=subprocess.PIPE)
                p.communicate(input=full_output.encode())
            except subprocess.CalledProcessError:
                pass

        elif selection == "2":
            print_color(">>> TARGETING HEAVY ASSETS...", Colors.BRRED)
            # expac -H M '%m\t%n' | sort -h -r | head -50
            cmd = "expac -H M '%m\t%n' | sort -h -r | head -50"
            subprocess.run(cmd, shell=True)

        elif selection == "3":
            print_color(">>> ACCESSING CHRONOLOGY...", Colors.BRGREEN)
            # expac --timefmt='%Y-%m-%d %T' '%l\t%n' | sort | tail -20
            cmd = "expac --timefmt='%Y-%m-%d %T' '%l\\t%n' | sort | tail -20"
            subprocess.run(cmd, shell=True)

        elif selection == "4":
            print_color(">>> SCANNING FOR ANOMALIES...", Colors.BRYELLOW)
            # expac '%n\t[%r]' | grep -v -E "core|extra" | sort
            cmd = "expac '%n\t[%r]' | grep -v -E 'core|extra' | sort"
            subprocess.run(cmd, shell=True)

        elif selection == "5":
            target_pkg = get_input("  >> ENTER TARGET ID: ", Colors.BRCYAN)

            # Check if package exists: pacman -Qq $target_pkg
            res = subprocess.run(["pacman", "-Qq", target_pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            if res.returncode == 0:
                print()
                print_color("  [ TARGET CONFIRMED ]", Colors.BRRED)

                fmt = """  NAME          : %n
  VERSION       : %v
  REPO          : %r
  SIZE          : %m
  URL           : %u
  BUILD DATE    : %t
  INSTALL DATE  : %l
  REASON        : %w
  ────────────────────────────────────────
  DEPENDENCIES  : %D
  ────────────────────────────────────────
  REQUIRED BY   : %N"""

                # expac -H M -l '\n                  * ' ...
                cmd = ["expac", "-H", "M", "-l", "\n                  * ", fmt, target_pkg]
                subprocess.run(cmd)
            else:
                print_color("  >> ERROR: TARGET UNKNOWN.", Colors.RED)

        elif selection == "0":
            print_color("  >> TERMINATING UPLINK.", Colors.RED)
            time.sleep(0.5)
            clear_screen()
            break

        else:
            print_color("  >> INVALID COMMAND.", Colors.RED)
            time.sleep(0.5)
            continue

        print()
        get_input("  [PRESS ENTER TO CONTINUE]", Colors.BRBLACK)

if __name__ == "__main__":
    main()
