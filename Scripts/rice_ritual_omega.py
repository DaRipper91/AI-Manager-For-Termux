#!/usr/bin/env python3
import time
import sys
import shutil
import subprocess

# --- VISUAL COMPLIANCE (ANSI ESCAPE CODES) ---
C_RED = "\033[91m"
C_CYAN = "\033[96m"
C_YELLOW = "\033[93m"
C_GREY = "\033[90m"
C_RESET = "\033[0m"
C_GREEN = "\033[92m"

def draw_splash():
    """Renders the Mandatory Valhalla Art"""
    print(f"{C_GREY}")
    print(r"""
      /\                                            /\
     /  \    ~*~  PROTOCOL OMEGA: THE SERPENT  ~*~    /  \
    /    \   <<[  TOTAL SYSTEM OVERWRITE  ]>>     /    \
   /  /\  \                                      /  /\  \
  /  /  \  \   (c) (c)   /\/\/\/\   (c) (c)     /  /  \  \
 /  /    \  \   \ \ \ \  \      /  / / / /     /  /    \  \
/  /      \  \   \ \ \ \  \    /  / / / /     /  /      \  \
\  \      /  /    ) ) ) )  (  )  ( ( ( (      \  \      /  /
 \  \    /  /    / / / /    \/    \ \ \ \      \  \    /  /
  \  \  /  /    (c) (c)            (c) (c)      \  \  /  /
   \  \/  /                                      \  \/  /
    \    /        >>  PYTHONIC BINDING  <<        \    /
     \  /                                          \  /
      \/                                            \/
    """)
    print(f"{C_CYAN}  > INITIALIZING SERPENT PROTOCOLS...{C_RESET}")
    time.sleep(0.5)
    print(f"{C_CYAN}  > THUMP... (Drumbeat){C_RESET}")
    time.sleep(0.5)

def run_command(command, description):
    """Executes a shell command with sarcasm and error handling"""
    print(f"{C_YELLOW}  >> {description}...{C_RESET}")
    try:
        # We use shell=True here to handle the argument parsing easily for complex AUR helpers
        # In a strict production env, we'd use a list, but for a rice script, this is efficient.
        subprocess.run(command, shell=True, check=True)
        print(f"{C_GREEN}     [SUCCESS] {description} applied.{C_RESET}")
    except subprocess.CalledProcessError:
        print(f"{C_RED}     [CRITICAL FAIL] The ritual failed at: {description}.{C_RESET}")
        print(f"{C_RED}     [ADVICE] Check your internet or your lock files, Jarl DaRipper.{C_RESET}")
        sys.exit(1)

def main():
    draw_splash()
    print(f"{C_RED}  > ENGAGING LOGIC CORE.{C_RESET}")
    time.sleep(1)

    # --- PHASE 1: DEPENDENCY CHECK ---
    print(f"{C_YELLOW}  ~*~ PHASE 1: SCANNING ARSENAL ~*~{C_RESET}")
    if shutil.which("yay") is None:
        print(f"{C_RED}  [ERROR] 'yay' not found. You are unprepared.{C_RESET}")
        sys.exit(1)

    # --- PHASE 2: ASSET ACQUISITION ---
    print(f"{C_YELLOW}  ~*~ PHASE 2: ACQUIRING ASSETS (AUR) ~*~{C_RESET}")
    packages = [
        "catppuccin-gtk-theme-mocha",
        "catppuccin-kde-arch-git",
        "papirus-icon-theme",
        "bibata-cursor-theme",
        "kvantum",
        "kvantum-theme-catppuccin-git",
        "ttf-jetbrains-mono-nerd",
        "ttf-nerd-fonts-symbols",
        "plasma-workspace" # Ensures tools like plasma-apply-globaltheme exist
    ]
    pkg_str = " ".join(packages)
    run_command(f"yay -S --noconfirm --needed {pkg_str}", "Downloading the Armory")

    # --- PHASE 3: CONFIGURATION INJECTION ---
    print(f"{C_YELLOW}  ~*~ PHASE 3: OVERWRITING REALITY (Config Injection) ~*~{C_RESET}")

    # Global Theme
    # Try the specific global theme name first, sometimes it varies by package version
    try:
        run_command("plasma-apply-globaltheme -a Catppuccin-Mocha-Global", "Injecting Global Theme")
    except SystemExit:
         print(f"{C_YELLOW}     [RETRY] Attempting fallback theme name...{C_RESET}")
         run_command("plasma-apply-globaltheme -a Catppuccin-Mocha", "Injecting Global Theme (Fallback)")

    # Icons
    run_command("/usr/lib/plasma-changeicons Papirus-Dark", "Replacing Icons (Papirus)")

    # Cursor
    run_command("plasma-apply-cursortheme Bibata-Modern-Ice", "Summoning Cursor")

    # Kvantum Setup
    run_command("kvantummanager --set Catppuccin-Mocha", "Configuring Kvantum Engine")
    run_command("kwriteconfig6 --file kdeglobals --group KDE --key widgetStyle kvantum", "Forcing Kvantum Style")

    # Fonts (Nerd Fonts)
    font_config = "JetBrainsMono NF,10,-1,5,50,0,0,0,0,0"
    run_command(f"kwriteconfig6 --file kdeglobals --group General --key font \"{font_config}\"", "Scribing UI Font")
    run_command(f"kwriteconfig6 --file kdeglobals --group General --key fixed \"{font_config}\"", "Scribing Fixed Font")
    run_command(f"kwriteconfig6 --file kdeglobals --group General --key menuFont \"{font_config}\"", "Scribing Menu Font")

    # --- PHASE 4: HASWELL OPTIMIZATION ---
    print(f"{C_RED}  ~*~ PHASE 4: OPTIMIZING FOR ANCIENT SILICON (HD 4600) ~*~{C_RESET}")

    # Disable Blur
    run_command("kwriteconfig6 --file kwinrc --group Plugins --key blurEnabled false", "Killing Blur (Saving GPU)")

    # Instant Animations
    run_command("kwriteconfig6 --file kdeglobals --group KDE --key AnimationDurationFactor 0", "Accelerating Time (Instant UI)")

    # Reload KWin
    print(f"{C_CYAN}  >> RELOADING WINDOW MANAGER...{C_RESET}")
    subprocess.run("qdbus6 org.kde.KWin /KWin reconfigure", shell=True)

    # --- EXIT ---
    print(f"{C_GREEN}")
    print("  ~*~ RITUAL COMPLETE ~*~")
    print("  > The Serpent has bitten. Your system is now compliant.")
    print("  > Log out and back in to see the full glory.")
    print(f"{C_RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C_RED}  [ABORT] You dare interrupt the ritual?{C_RESET}")
        sys.exit(130)
