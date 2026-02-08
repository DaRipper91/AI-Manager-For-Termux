# Arch Linux Installer

This tool provides a terminal-based user interface (TUI) to help you install packages and restore settings on a fresh Arch Linux installation.

## How to Use

1.  **Run the main script:**
    ```bash
    cd arch-installer
    ./main.sh
    ```

2.  **Navigate the menus:**
    Use the arrow keys to navigate the menus and press Enter to select an option. You can use the spacebar to select or deselect items in checklists.

## Menu Options

*   **Packages:** Install packages from the official Arch Linux repositories. You will be presented with a checklist of packages found in the `data/packages.list` file.
*   **AUR:** Install packages from the Arch User Repository (AUR). This will automatically install the `yay` AUR helper if it's not already present. You will be presented with a checklist of packages found in the `data/aur.list` file.
*   **Dotfiles:** Restore your configuration files (dotfiles). You will be presented with a checklist of files and directories found in the `assets/dotfiles` directory. Existing files will be backed up with a `.bak` extension.
*   **All:** Run all the above installation steps in sequence.

## Backing Up Your Settings

Before you can restore your settings on a new system, you need to back them up from your current system.

1.  **Run the backup script:**
    ```bash
    ./backup_dotfiles.sh
    ```

2.  **Review the backed-up files:**
    The script will copy your configuration files into the `assets/dotfiles` directory. It is highly recommended that you review the contents of this directory and remove any unnecessary or sensitive files before transferring this tool to a new system.
