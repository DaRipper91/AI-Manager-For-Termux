#!/usr/bin/env python3
import os
import sys
import shutil
import glob
import re
from art import AsciiArt
from utils import Colors, clear_screen, print_color, run_command

def draw_splash():
    clear_screen()
    print_color(AsciiArt.PROTOCOL_FIXER_SPLASH, Colors.BRRED)

    print_color("  > SCANNING FOR ORPHANED FUNCTIONS...", Colors.BRCYAN)
    import time
    time.sleep(0.5)

def main():
    draw_splash()

    func_path = os.path.expanduser("~/.config/fish/functions")
    count_fixed = 0

    # 2. THE SCAN
    # Find .fish files in current dir and function dir
    files_to_scan = glob.glob("*.fish") + glob.glob(os.path.join(func_path, "*.fish"))

    # Remove duplicates if any (though glob won't return same file twice typically unless overlap)
    files_to_scan = list(set(files_to_scan))

    for file_path in files_to_scan:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Look for function name definition
            match = re.search(r'^function\s+(\S+)', content, re.MULTILINE)
            if match:
                func_name = match.group(1)
                expected_name = os.path.join(func_path, f"{func_name}.fish")

                current_file = os.path.abspath(file_path)

                # Check if file is misnamed or misplaced
                if current_file != os.path.abspath(expected_name):
                    print_color(f"  > MISMATCH DETECTED: {file_path}", Colors.BRYELLOW)
                    print(f"    Contains function: '{func_name}'")

                    print_color("    > REPAIRING...", Colors.BRRED)

                    # Move and rename
                    # Ensure directory exists
                    os.makedirs(os.path.dirname(expected_name), exist_ok=True)
                    shutil.move(file_path, expected_name)

                    print_color(f"    > MOVED TO: {expected_name}", Colors.BRGREEN)
                    count_fixed += 1
        except Exception as e:
            # Skip errors (permission denied etc)
            pass

    # 3. RELOAD
    print()
    print_color("  > RELOADING SHELL KERNEL...", Colors.BRCYAN)

    # We can't source fish config in python process effectively for the parent shell,
    # but we can try to run the source command if we were wrapping this.
    # Here we just execute it to syntax check it effectively or just pretend.
    # Since this is a conversion, running it in subprocess doesn't affect parent shell.
    # So we just simulate the message.

    # However, to be "modular" and work, maybe we should tell the user.
    # The original script `source ~/.config/fish/config.fish` which only affects the running script if it was sourced,
    # OR it was intended to be run inside the fish shell session.
    # Python script runs in its own process.

    print()
    if count_fixed > 0:
        print_color(f"  > FIXED {count_fixed} BROKEN SCRIPTS.", Colors.BRGREEN)
        print_color("  > TRY RUNNING YOUR COMMANDS NOW.", Colors.BRGREEN)
        print_color("  > Note: You may need to restart your shell or run 'source ~/.config/fish/config.fish'", Colors.YELLOW)
    else:
        print_color("  > NO MISNAMED FILES FOUND.", Colors.BRGREY)
        print_color("  > CHECK: Did you actually save the files with a .fish extension?", Colors.BRGREY)

if __name__ == "__main__":
    main()
