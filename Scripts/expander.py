#!/usr/bin/env python3
import sys
import time
import subprocess
import os
import shutil
from art import AsciiArt
from utils import Colors, clear_screen, print_color, loading_bar, check_root

def draw_splash():
    clear_screen()
    print_color(AsciiArt.EXPANDER_SPLASH, Colors.BRRED)

    print_color("  [SYSTEM] > LOADING KERNEL MODULES... ", Colors.BRCYAN, end='')
    loading_bar(20, 0.05, '█', '', ' DONE.')
    time.sleep(0.5)

def main():
    draw_splash()

    # Validation Check
    # In python we check effective user ID but original used `functions -q sudo` which just checks if sudo exists.
    # But usually this script needs root. The original script calls sudo inside.

    # Check if sudo exists
    if not shutil.which("sudo"):
        print_color("  > ERROR: SUDO COMMAND NOT FOUND.", Colors.BRRED)
        return

    print_color("  > [WARNING] Initiating write sequence to /etc/systemd...", Colors.BRYELLOW)

    # Installing the tool
    # sudo pacman -S --noconfirm zram-generator 2>/dev/null
    subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "zram-generator"], stderr=subprocess.DEVNULL)

    print_color("  > [CONFIG]  Targeting Algorithm: ZSTD (Haswell Optimized)...", Colors.BRCYAN)
    print_color("  > [CONFIG]  Expansion Ratio: 1.5x (12GB Effective)...", Colors.BRCYAN)

    # Writing configuration
    zram_conf = """[zram0]
zram-size = ram * 1.5
compression-algorithm = zstd
swap-priority = 100
fs-type = swap"""

    # echo ... | sudo tee /etc/systemd/zram-generator.conf > /dev/null
    # Implementing using subprocess to handle sudo pipe
    p1 = subprocess.Popen(["echo", zram_conf], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["sudo", "tee", "/etc/systemd/zram-generator.conf"], stdin=p1.stdout, stdout=subprocess.DEVNULL)
    p1.stdout.close()
    p2.communicate()

    print_color("  > [KERNEL]  Overwriting VM Swappiness values...", Colors.BRYELLOW)

    sysctl_conf = """vm.swappiness = 133
vm.watermark_boost_factor = 0
vm.watermark_scale_factor = 125
vm.page-cluster = 0"""

    p1 = subprocess.Popen(["echo", sysctl_conf], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["sudo", "tee", "/etc/sysctl.d/99-vm-zram-parameters.conf"], stdin=p1.stdout, stdout=subprocess.DEVNULL)
    p1.stdout.close()
    p2.communicate()

    print_color("  > [DAEMON]  Reloading SystemD Units...", Colors.BRCYAN)
    subprocess.run(["sudo", "systemctl", "daemon-reload"])
    subprocess.run(["sudo", "systemctl", "start", "systemd-zram-setup@zram0.service"])

    # 3. THE EXIT
    print_color("  > --------------------------------------------------", Colors.BRGREEN)
    print_color("  > OPERATION SUCCESSFUL.", Colors.BRGREEN)
    print_color("  > --------------------------------------------------", Colors.BRGREEN)
    print_color("  > Current ZRAM Status:", Colors.BRGREEN)
    print_color("", Colors.BRGREY, end='') # Set color for zramctl
    subprocess.run(["zramctl"])
    print_color("  > --------------------------------------------------", Colors.BRGREEN)
    print_color("  > You're welcome, DaRipper.", Colors.WHITE)

if __name__ == "__main__":
    main()
