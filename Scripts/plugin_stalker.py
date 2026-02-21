#!/usr/bin/env python3
import sys
import time
import subprocess
import os
import glob
from art import AsciiArt
from utils import Colors, clear_screen, print_color, loading_bar

def draw_splash():
    clear_screen()
    print_color(AsciiArt.PLUGIN_STALKER_SPLASH, Colors.BRRED)

    print_color("  > CALIBRATING LONG-RANGE SENSORS ", Colors.BRCYAN, end='')
    loading_bar(5, 0.04, '█', '', ' [LOCKED]')
    time.sleep(0.3)

def main():
    draw_splash()

    # 2. TARGET ACQUISITION
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
        # Original script used $__fish_config_dir which defaults to ~/.config/fish usually?
        # But here it says "Defaulting to local config base".
        # Let's assume ~/.config/fish for now or just ~/.config.
        # Wait, if I look at fish documentation, __fish_config_dir is usually ~/.config/fish

        # However, the script says "Defaulting to local config base."
        # If I look at the script logic later: `set manifests (find "$target_dir" -name "fish_plugins" ...)`
        # `fish_plugins` is usually in `~/.config/fish/`.

        # Let's default to ~/.config/fish if it exists, otherwise ~/.config
        potential_fish = os.path.expanduser("~/.config/fish")
        if os.path.isdir(potential_fish):
            target_dir = potential_fish
        else:
            target_dir = os.path.expanduser("~/.config")

        print_color("  > No target specified. Defaulting to local config base.", Colors.BRGREY)

    if not os.path.isdir(target_dir):
        print_color(f"  > [ERROR] Target directory '{target_dir}' does not exist.", Colors.BRRED)
        print_color("  > Are you hallucinating folders again?", Colors.BRRED)
        sys.exit(1)

    if len(sys.argv) > 1:
        print_color(f"  > OVERRIDE DETECTED. Targeting sector: {target_dir}", Colors.BRYELLOW)

    print_color("  > INFILTRATING FILE SYSTEM ", Colors.NORMAL, end='')
    loading_bar(5, 0.04, '▒', '', ' [ACCESS GRANTED]')
    time.sleep(0.4)

    # --- SECTOR 1: MANIFEST HUNT (fish_plugins) ---
    print()
    print_color("  ╔════════════════════════════════════════╗", Colors.BRYELLOW)
    print_color("  ║ SECTOR 1: MANIFEST RECOVERY            ║", Colors.BRYELLOW)
    print_color("  ╚════════════════════════════════════════╝", Colors.BRYELLOW)

    # Find all 'fish_plugins' files recursively
    manifests = []
    for root, dirs, files in os.walk(target_dir):
        if "fish_plugins" in files:
            manifests.append(os.path.join(root, "fish_plugins"))

    man_count = len(manifests)

    if man_count > 0:
        print_color(f"  > Detected {man_count} plugin manifest(s).", Colors.BRCYAN)

        for file_path in manifests:
            print()
            print_color(f"    [SOURCE] {file_path}", Colors.BRRED)
            print_color("    ------------------------------------", Colors.BRGREY)

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    contents = [line.strip() for line in f if line.strip()]

                if not contents:
                    print("    (Empty File)")
                else:
                    for line in contents:
                        if "theme" in line:
                            print_color(f"    [THEME]  {line}", Colors.BRMAGENTA)
                        else:
                            print_color(f"    [PLUGIN] {line}", Colors.BRGREEN)
            except Exception:
                 print("    (Read Error)")
    else:
        print_color("  > No 'fish_plugins' manifests found in this sector.", Colors.BRGREY)

    # --- SECTOR 2: ROGUE SCRIPT SCAN ---
    print()
    print_color("  ╔════════════════════════════════════════╗", Colors.BRYELLOW)
    print_color("  ║ SECTOR 2: DEEP CONTENT ANALYSIS        ║", Colors.BRYELLOW)
    print_color("  ╚════════════════════════════════════════╝", Colors.BRYELLOW)
    print("  > Scanning .fish files for 'theme' or 'plugin' keywords...")

    cmd = ["grep", "-rnE", "--color=always", "theme|plugin", target_dir, "--include=*.fish"]

    try:
        # We need to capture output and head it.
        # But grep returns exit code 1 if not found.
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        # We read lines and limit to 15
        hits = []
        for i, line in enumerate(proc.stdout):
            if i >= 15:
                break
            hits.append(line.strip())
        proc.terminate()

        hit_count = len(hits) # Note: this is just what we captured, might be more.
        # But for logic we just care if > 0.

        if hit_count > 0:
            print_color(f"  > KEYWORD HITS DETECTED ({hit_count}+):", Colors.BRRED)
            print()
            for hit in hits:
                print(f"    {hit}")
                time.sleep(0.05)

            if hit_count == 15:
                print_color("    ... (Scan limit reached. Too much noise.)", Colors.BRYELLOW)
        else:
            print_color("  > No loose keywords found. Sector appears clean.", Colors.BRCYAN)

    except Exception:
         print_color("  > No loose keywords found. Sector appears clean.", Colors.BRCYAN)

    # --- SECTOR 3: THEME FOLDER RECON ---
    print()
    print_color("  ╔════════════════════════════════════════╗", Colors.BRYELLOW)
    print_color("  ║ SECTOR 3: DIRECTORY STRUCTURE          ║", Colors.BRYELLOW)
    print_color("  ╚════════════════════════════════════════╝", Colors.BRYELLOW)

    # Look for folders named "themes" or "functions" or "conf.d"

    folders_found = []
    # We can use os.walk again but find is more direct for depth search if unlimited depth?
    # Original used find without maxdepth, so recursive.

    # Implementing a limited find in python
    count = 0
    for root, dirs, files in os.walk(target_dir):
        for d in dirs:
            if d in ["themes", "functions", "conf.d"]:
                folders_found.append(os.path.join(root, d))
                count += 1
                if count >= 5:
                    break
        if count >= 5:
            break

    if folders_found:
        print_color("  > CRITICAL INFRASTRUCTURE FOUND:", Colors.BRGREEN)
        for folder in folders_found:
            print(f"    [DIR] {folder}")
            try:
                items = os.listdir(folder)[:3]
                for item in items:
                    print_color(f"       └─ {item}", Colors.BRGREY)
            except OSError:
                pass
    else:
        print_color("  > No standard config folders found.", Colors.BRGREY)

    # 3. THE EXIT
    print()
    print_color("  ══════════════════════════════════════════", Colors.BRRED)
    print_color("  > DEEP SCAN COMPLETE.", Colors.BRRED)

if __name__ == "__main__":
    main()
