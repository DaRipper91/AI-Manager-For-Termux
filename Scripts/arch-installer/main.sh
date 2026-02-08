#!/bin/bash
# main.sh - A TUI for installing packages and settings on a fresh Arch install.

# --- Color Definitions ---
export NC='\033[0m' # No Color (resets to default terminal color, usually white/light gray)
export WHITE='\033[1;37m' # Bright White for common text
export RED='\033[0;31m' # Red for errors (standard)

# Pastel-like colors using bright ANSI codes
export PASTEL_TEAL='\033[1;36m'      # Bright Cyan
export PASTEL_PURPLE='\033[1;35m'    # Bright Magenta
export PASTEL_LIGHTBLUE='\033[1;34m' # Bright Blue
export PASTEL_LIGHTGREEN='\033[1;32m'# Bright Green
export PASTEL_YELLOW='\033[1;33m'   # Bright Yellow

# --- Configuration ---
DIALOG_CANCEL=1
DIALOG_ESC=255
DIALOG_HEIGHT=20
DIALOG_WIDTH=60

# --- Dependency Check ---
if ! command -v dialog &> /dev/null; then
    echo -e "${RED}dialog is not installed. Please install it to continue.${NC}"
    echo -e "${PASTEL_YELLOW}You can install it with: sudo pacman -S dialog${NC}"
    exit 1
fi

# --- Functions ---
show_header() {
    clear
    echo -e "${PASTEL_TEAL}"
    echo " d8888b.  .d8b.  d8888b. db    db d88888b d88888b d8888b.   d888b."
    echo " 88  \`8D d8' \`8b 88  \`8D 88    88 88'     88'     88  \`8D  88'  YP"
    echo " 88   88 88ooo88 88oobY' 88    88 88ooooo 88ooooo 88   88  \`8bo."
    echo " 88   88 88~~~88 88\`8b   88    88 88~~~~~ 88~~~~~ 88   88    \`Y8b."
    echo " 88  .8D 88   88 88 \`88. 88b  d88 88.     88.     88  .8D  db   8D"
    echo " Y8888D' YP   YP 88   YD ~Y8888P' Y88888P Y88888P Y8888D'  \`8888Y'"
    echo -e "${NC}"
    echo -e "${PASTEL_LIGHTBLUE}==================================================================="
    echo -e "${WHITE}   A TUI for installing packages and settings on a fresh Arch install   ${NC}"
    echo -e "${PASTEL_LIGHTBLUE}==================================================================="
    echo
}

show_main_menu() {
    exec 3>&1
    selection=$(dialog \
        --backtitle "${PASTEL_TEAL}daripper os Installer${NC}" \
        --title "${PASTEL_PURPLE}Main Menu${NC}" \
        --clear \
        --cancel-label "Exit" \
        --menu "Please select an option:" \
        $DIALOG_HEIGHT $DIALOG_WIDTH 4 \
        "Packages" "Install packages from official repositories" \
        "AUR" "Install packages from the AUR" \
        "Dotfiles" "Restore configuration files" \
        "All" "Run all installation steps" \
        2>&1 1>&3)
    exit_status=$?
    exec 3>&-

    case $exit_status in
        $DIALOG_CANCEL)
            clear
            echo -e "${WHITE}Program terminated.${NC}"
            exit
            ;;
        $DIALOG_ESC)
            clear
            echo -e "${RED}Program aborted.${NC}"
            exit 1
            ;;
    esac

    case $selection in
        "Packages")
            ./modules/01-packages.sh
            ;;
        "AUR")
            ./modules/02-aur.sh
            ;;
        "Dotfiles")
            ./modules/03-dotfiles.sh
            ;;
        "All")
            dialog --backtitle "${PASTEL_TEAL}daripper os Installer${NC}" --title "${PASTEL_PURPLE}Confirmation${NC}" --yesno "${WHITE}This will run all installation steps: Packages, AUR, and Dotfiles. Continue?${NC}" 10 50
            if [ $? -eq 0 ]; then
                ./modules/01-packages.sh
                ./modules/02-aur.sh
                ./modules/03-dotfiles.sh
                dialog --backtitle "${PASTEL_TEAL}daripper os Installer${NC}" --title "${PASTEL_LIGHTGREEN}Complete${NC}" --msgbox "${WHITE}All installation steps completed.${NC}" 8 40
            fi
            ;;
    esac
}

# --- Main ---
while true; do
    show_header
    show_main_menu
done
