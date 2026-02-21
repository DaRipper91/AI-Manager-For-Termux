#!/usr/bin/env python3
import sys
import os
import subprocess
import shutil
import time

# Ensure we can import modules from the same directory
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir)

try:
    from utils import Colors, print_color, clear_screen, run_command
    from art import AsciiArt
except ImportError:
    print("Error: Could not import utils or art modules. Make sure you are running this from the Scripts directory or root.")
    sys.exit(1)

class Dialog:
    def __init__(self):
        if shutil.which("dialog") is None:
            raise EnvironmentError("dialog is not installed. Please install 'dialog'.")

    def _run(self, args):
        cmd = ["dialog"] + args
        # dialog writes result to stderr
        result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
        return result.returncode, result.stderr

    def msgbox(self, title, text, height=8, width=50):
        self._run(["--backtitle", "Universal Installer", "--title", title, "--msgbox", text, str(height), str(width)])

    def infobox(self, title, text, height=8, width=50):
        subprocess.run(["dialog", "--backtitle", "Universal Installer", "--title", title, "--infobox", text, str(height), str(width)])

    def yesno(self, title, text, height=8, width=50):
        code, _ = self._run(["--backtitle", "Universal Installer", "--title", title, "--yesno", text, str(height), str(width)])
        return code == 0

    def menu(self, title, text, options, height=15, width=60, menu_height=10):
        # options is list of tuples (tag, item)
        args = ["--backtitle", "Universal Installer", "--title", title, "--menu", text, str(height), str(width), str(menu_height)]
        for tag, item in options:
            args.extend([tag, item])
        code, output = self._run(args)
        if code == 0:
            return output.strip()
        return None

    def checklist(self, title, text, options, height=20, width=70, list_height=10):
        # options: (tag, item, status)
        args = ["--backtitle", "Universal Installer", "--title", title, "--checklist", text, str(height), str(width), str(list_height)]
        for tag, item, status in options:
            args.extend([tag, item, status])

        # We need to capture stderr carefully because checklist returns list of quoted strings
        # But for simple tags, it might be okay.
        code, output = self._run(args)
        if code == 0:
            # Output looks like "tag1" "tag2" ...
            import shlex
            try:
                return shlex.split(output)
            except:
                return output.split()
        return None

def detect_environment():
    # Termux check
    if "com.termux" in os.environ.get("PREFIX", "") or os.environ.get("TERMUX_VERSION"):
        return "TERMUX"

    # Arch check
    if os.path.exists("/etc/arch-release"):
        return "ARCH"

    # Fallback checks
    try:
        with open("/etc/os-release") as f:
            content = f.read()
            if "ID=cachyos" in content or "ID_LIKE=arch" in content:
                return "ARCH"
    except FileNotFoundError:
        pass

    return "UNKNOWN"

def install_termux_arch(d):
    d.infobox("Termux Setup", "Installing Arch Linux via proot-distro...\nThis may take a while.")

    commands = [
        ("Installing Dependencies", "pkg update -y && pkg install -y proot-distro termux-x11-nightly git"),
        ("Installing Arch Linux", "proot-distro install archlinux")
    ]

    for desc, cmd in commands:
        clear_screen()
        print_color(f" >> {desc}...", Colors.BRCYAN)
        res = subprocess.run(cmd, shell=True)
        if res.returncode != 0:
            d.msgbox("Error", f"Failed to run: {desc}")
            return

    d.msgbox("Success", "Arch Linux installed successfully!\nYou can now start it from the main menu.")

def start_termux_arch(d):
    clear_screen()
    print_color(" >> Starting Arch Linux...", Colors.BRGREEN)
    subprocess.run("proot-distro login archlinux", shell=True)

def install_desktop_environment(d):
    des = [
        ("KDE", "Plasma Desktop (Full)", "off"),
        ("GNOME", "GNOME Desktop", "off"),
        ("Hyprland", "Hyprland Wayland Compositor", "off"),
        ("XFCE", "XFCE4 Desktop (Lightweight)", "off"),
        ("Cinnamon", "Cinnamon Desktop", "off")
    ]

    # Use radiolist for single choice, or checklist for multiple? Usually one DE is enough, but user might want multiple.
    # Let's stick to menu for single choice to avoid conflicts, or checklist if user knows what they are doing.
    # Menu is safer for "Install DE".

    choice = d.menu("Desktop Environment", "Select a Desktop Environment to install:",
                    [(x[0], x[1]) for x in des])

    if not choice:
        return

    packages = []
    if choice == "KDE":
        packages = ["plasma-meta", "konsole", "dolphin"]
    elif choice == "GNOME":
        packages = ["gnome", "gnome-extra"]
    elif choice == "Hyprland":
        packages = ["hyprland", "waybar", "kitty"]
    elif choice == "XFCE":
        packages = ["xfce4", "xfce4-goodies"]
    elif choice == "Cinnamon":
        packages = ["cinnamon"]

    if d.yesno("Confirm", f"Install {choice} and related packages?\n\nPackages: {', '.join(packages)}"):
        cmd = f"sudo pacman -S --needed {' '.join(packages)}"
        clear_screen()
        print_color(f" >> Installing {choice}...", Colors.BRCYAN)
        subprocess.run(cmd, shell=True)
        d.msgbox("Done", f"{choice} installation complete.")

def install_packages(d):
    pkg_list_file = os.path.join(script_dir, "arch-installer/data/packages.list")
    if not os.path.exists(pkg_list_file):
        d.msgbox("Error", f"Package list not found at:\n{pkg_list_file}")
        return

    with open(pkg_list_file, 'r') as f:
        pkgs = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    # Create checklist options
    # Limit list size or use a scrolled dialog
    # dialog checklist handles scrolling
    options = [(pkg, "", "on") for pkg in pkgs]

    selection = d.checklist("Package Selection", "Select packages to install:", options, height=25)

    if not selection:
        return

    if d.yesno("Confirm", f"Install {len(selection)} packages?"):
        cmd = ["sudo", "pacman", "-S", "--needed", "--noconfirm"] + selection
        clear_screen()
        print_color(" >> Installing selected packages...", Colors.BRCYAN)
        subprocess.run(cmd)
        d.msgbox("Done", "Packages installed.")

def run_rice_ritual(d):
    rice_script = os.path.join(script_dir, "rice_ritual_omega.py")
    if not os.path.exists(rice_script):
        d.msgbox("Error", "Rice ritual script not found.")
        return

    clear_screen()
    subprocess.run([sys.executable, rice_script])
    print_color("\nPress Enter to return to menu...", Colors.BRGREY)
    input()

def main():
    try:
        d = Dialog()
    except EnvironmentError as e:
        print_color(f"Error: {e}", Colors.RED)
        print_color("Please install 'dialog' package.", Colors.YELLOW)
        sys.exit(1)

    env = detect_environment()

    while True:
        # Show Splash (briefly or just as header check)
        # Using dialog, we don't show stdout splash easily unless we use --infobox before menu
        # But we can just go straight to menu.

        if env == "TERMUX":
            options = [
                ("1", "Install Arch (Proot + X11)"),
                ("2", "Start Arch Linux"),
                ("3", "Exit")
            ]
            choice = d.menu("Main Menu (Termux)", "Select an option:", options)

            if choice == "1":
                install_termux_arch(d)
            elif choice == "2":
                start_termux_arch(d)
            elif choice == "3" or choice is None:
                break

        elif env == "ARCH":
            options = [
                ("1", "Install Desktop Environment"),
                ("2", "Install Packages"),
                ("3", "Run Rice Ritual (Omega)"),
                ("4", "Exit")
            ]
            choice = d.menu("Main Menu (Arch/CachyOS)", "Select an option:", options)

            if choice == "1":
                install_desktop_environment(d)
            elif choice == "2":
                install_packages(d)
            elif choice == "3":
                run_rice_ritual(d)
            elif choice == "4" or choice is None:
                break
        else:
            d.msgbox("Unknown Environment", "Could not detect Termux or Arch Linux.\nRunning in generic mode.")
            env = "ARCH" # Fallback to Arch menu for testing or generic usage
            continue

    clear_screen()
    print_color("Goodbye!", Colors.BRGREEN)

if __name__ == "__main__":
    main()
