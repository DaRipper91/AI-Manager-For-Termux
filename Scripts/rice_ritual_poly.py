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
C_PURPLE = "\033[95m"

# --- THEME MATRIX (THE ARMORY) ---
THEME_MATRIX = {
    "1": {
        "name": "Catppuccin Mocha (The Standard)",
        "packages": [
            "catppuccin-gtk-theme-mocha",
            "catppuccin-kde-arch-git",
            "kvantum-theme-catppuccin-git"
        ],
        "global_theme": "Catppuccin-Mocha-Global",
        "kvantum_theme": "Catppuccin-Mocha",
        "cursor": "Bibata-Modern-Ice",
        "icons": "Papirus-Dark"
    },
    "2": {
        "name": "Nordic (The Valhalla Ice)",
        "packages": [
            "nordic-theme",
            "nordic-kde-git",
            "kvantum-theme-nordic-git"
        ],
        "global_theme": "Nordic",
        "kvantum_theme": "Nordic",
        "cursor": "Bibata-Modern-Ice",
        "icons": "Papirus-Dark"
    },
    "3": {
        "name": "Dracula (The Vampire)",
        "packages": [
            "dracula-gtk-theme",
            "dracula-kde-theme-git",
            "kvantum-theme-dracula-git"
        ],
        "global_theme": "Dracula",
        "kvantum_theme": "Dracula",
        "cursor": "Bibata-Modern-Ice",
        "icons": "Papirus-Dark"
    },
    "4": {
        "name": "Tokyo Night (The Neon City)",
        "packages": [
            "tokyo-night-gtk-theme-git",
            "tokyo-night-kde-git",
            "kvantum-theme-tokyo-night-git"
        ],
        "global_theme": "Tokyo-Night",
        "kvantum_theme": "Tokyo-Night",
        "cursor": "Bibata-Modern-Ice",
        "icons": "Papirus-Dark"
    },
    "5": {
        "name": "Gruvbox (The Retro Bunker)",
        "packages": [
            "gruvbox-material-gtk-theme-git",
            "gruvbox-material-kde-git",
            "kvantum-theme-gruvbox-git"
        ],
        "global_theme": "Gruvbox-Material-Dark",
        "kvantum_theme": "Gruvbox-Material-Dark",
        "cursor": "Bibata-Modern-Amber",
        "icons": "Papirus-Dark"
    }
}

def draw_splash():
    """Renders the Mandatory Valhalla Art (Sanitized)"""
    # NOTE: Double backslashes are used here to prevent SyntaxErrors
    print(f"{C_GREY}")
    print("""
      /\\                                            /\\
     /  \\    ~*~  PROTOCOL OMEGA: POLY-THEME   ~*~    /  \\
    /    \\   <<[  CHOOSE YOUR VISUAL REALITY  ]>>     /    \\
   /  /\\  \\                                      /  /\\  \\
  /  /  \\  \\   (c) (c)   /\\/\\/\\/\\   (c) (c)     /  /  \\  \\
 /  /    \\  \\   \\ \\ \\ \\  \\      /  / / / /     /  /    \\  \\
/  /      \\  \\   \\ \\ \\ \\  \\    /  / / / /     /  /      \\  \\
\\  \\      /  /    ) ) ) )  (  )  ( ( ( (      \\  \\      /  /
 \\  \\    /  /    / / / /    \\/    \\ \\ \\ \\      \\  \\    /  /
  \\  \\  /  /    (c) (c)            (c) (c)      \\  \\  /  /
   \\  \\/  /                                      \\  \\/  /
    \\    /        >>  THE SERPENT WAITS   <<      \\    /
     \\  /                                          \\  /
      \\/                                            \\/
    """)
    print(f"{C_CYAN}  > INITIALIZING SERPENT PROTOCOLS...{C_RESET}")
    time.sleep(0.5)

def run_command(command, description):
    """Executes a shell command with sarcasm and error handling"""
    print(f"{C_YELLOW}  >> {description}...{C_RESET}")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"{C_GREEN}     [SUCCESS] {description} applied.{C_RESET}")
    except subprocess.CalledProcessError:
        print(f"{C_RED}     [CRITICAL FAIL] The ritual failed at: {description}.{C_RESET}")
        print(f"{C_RED}     [ADVICE] Check the AUR. Sometimes packages die.{C_RESET}")
        if "yay" in command:
            sys.exit(1)

def select_theme():
    print(f"{C_PURPLE}  ~*~ AVAILABLE REALITY FILTERS ~*~{C_RESET}")
    for key, data in THEME_MATRIX.items():
        print(f"  [{key}] {data['name']}")

    choice = input(f"\n{C_CYAN}  > Select your Protocol (1-5): {C_RESET}")

    if choice in THEME_MATRIX:
        return THEME_MATRIX[choice]
    else:
        print(f"{C_RED}  [ERROR] Invalid Choice. Defaulting to Catppuccin (Safety Protocol).{C_RESET}")
        return THEME_MATRIX["1"]

def main():
    draw_splash()
    print(f"{C_RED}  > ENGAGING LOGIC CORE.{C_RESET}")

    # --- PHASE 0: SELECTION ---
    SELECTED_THEME = select_theme()
    print(f"{C_GREEN}  > TARGET LOCKED: {SELECTED_THEME['name']}{C_RESET}")
    time.sleep(1)

    # --- PHASE 1: DEPENDENCY CHECK ---
    print(f"{C_YELLOW}  ~*~ PHASE 1: SCANNING ARSENAL ~*~{C_RESET}")
    if shutil.which("yay") is None:
        print(f"{C_RED}  [ERROR] 'yay' not found. You are unprepared.{C_RESET}")
        sys.exit(1)

    # --- PHASE 2: ASSET ACQUISITION ---
    print(f"{C_YELLOW}  ~*~ PHASE 2: ACQUIRING ASSETS (AUR) ~*~{C_RESET}")

    # Base packages every theme needs
    base_packages = [
        "papirus-icon-theme",
        "bibata-cursor-theme",
        "kvantum",
        "ttf-jetbrains-mono-nerd",
        "ttf-nerd-fonts-symbols",
        "plasma-workspace"
    ]

    # Combine base + theme specific packages
    all_packages = base_packages + SELECTED_THEME["packages"]
    pkg_str = " ".join(all_packages)

    run_command(f"yay -S --noconfirm --needed {pkg_str}", f"Downloading {SELECTED_THEME['name']} Assets")

    # --- PHASE 3: CONFIGURATION INJECTION ---
    print(f"{C_YELLOW}  ~*~ PHASE 3: OVERWRITING REALITY (Config Injection) ~*~{C_RESET}")

    # 1. Global Theme
    try:
        run_command(f"plasma-apply-globaltheme -a {SELECTED_THEME['global_theme']}", "Injecting Global Theme")
    except:
        print(f"{C_YELLOW}     [WARN] Exact theme name match failed. Check System Settings manually.{C_RESET}")

    # 2. Icons
    run_command(f"/usr/lib/plasma-changeicons {SELECTED_THEME['icons']}", f"Replacing Icons ({SELECTED_THEME['icons']})")

    # 3. Cursor
    run_command(f"plasma-apply-cursortheme {SELECTED_THEME['cursor']}", f"Summoning Cursor ({SELECTED_THEME['cursor']})")

    # 4. Kvantum Setup
    run_command(f"kvantummanager --set {SELECTED_THEME['kvantum_theme']}", "Configuring Kvantum Engine")
    run_command("kwriteconfig6 --file kdeglobals --group KDE --key widgetStyle kvantum", "Forcing Kvantum Style")

    # 5. Fonts (Nerd Fonts) - Universal
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
    print(f"  > The {SELECTED_THEME['name']} Protocol is active.")
    print("  > Log out and back in to finalize the render.")
    print(f"{C_RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C_RED}  [ABORT] Cowardice detected.{C_RESET}")
        sys.exit(130)
