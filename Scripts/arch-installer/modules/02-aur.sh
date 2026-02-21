#!/bin/bash
# modules/02-aur.sh - Install packages from the AUR.

# --- Configuration ---
SCRIPT_DIR=$(dirname "$(realpath "$0")")
DATA_FILE="$SCRIPT_DIR/../data/aur.list"
DIALOG_HEIGHT=25
DIALOG_WIDTH=70

# --- Functions ---
install_yay() {
    if ! command -v yay &> /dev/null; then
        dialog --backtitle "${PASTEL_TEAL}daripper os Installer${NC}" --title "${PASTEL_LIGHTBLUE}Installation${NC}" --infobox "${WHITE}yay is not installed. Installing it now...${NC}" 5 40
        (
            sudo pacman -S --needed --noconfirm git base-devel && \
            cd /tmp && \
            git clone https://aur.archlinux.org/yay.git && \
            cd yay && \
            makepkg -si --noconfirm
        ) | dialog --progressbox "${WHITE}Installing yay...${NC}" 20 70
        if ! command -v yay &> /dev/null; then
            dialog --backtitle "${PASTEL_TEAL}daripper os Installer${NC}" --title "${RED}Error${NC}" --msgbox "${WHITE}Failed to install yay. Please install it manually.${NC}" 8 40
            exit 1
        fi
    fi
}

# --- Main ---
install_yay

if [ ! -f "$DATA_FILE" ]; then
    dialog --backtitle "${PASTEL_TEAL}daripper os Installer${NC}" --title "${RED}Error${NC}" --msgbox "${WHITE}AUR package list file not found: $DATA_FILE${NC}" 8 40
    exit 1
fi

# Prepare the package list for the checklist dialog
mapfile -t packages < "$DATA_FILE"
options=()
for pkg in "${packages[@]}"; do
    options+=("$pkg" "" "on")
done

# Show the checklist dialog
exec 3>&1
selection=$(dialog \
    --separate-output \
    --backtitle "${PASTEL_TEAL}daripper os Installer${NC}" \
    --title "${PASTEL_PURPLE}AUR Package Selection${NC}" \
    --checklist "${WHITE}Select AUR packages to install:${NC}" \
    $DIALOG_HEIGHT $DIALOG_WIDTH 15 \
    "${options[@]}" \
    2>&1 1>&3)
exit_status=$?
exec 3>&-

if [ $exit_status -ne 0 ]; then
    exit
fi

if [ -z "$selection" ]; then
    dialog --backtitle "${PASTEL_TEAL}daripper os Installer${NC}" --title "${PASTEL_YELLOW}Warning${NC}" --msgbox "${WHITE}No packages selected.${NC}" 8 40
    exit
fi

# Read selection into an array
mapfile -t selected_packages <<< "$selection"

# Install the selected packages
dialog --backtitle "${PASTEL_TEAL}daripper os Installer${NC}" --title "${PASTEL_LIGHTBLUE}Installation${NC}" --infobox "${WHITE}Installing selected AUR packages...${NC}" 5 40
yay -S --noconfirm --needed "${selected_packages[@]}" | dialog --progressbox "${WHITE}Installing AUR packages...${NC}" 20 70

dialog --backtitle "${PASTEL_TEAL}daripper os Installer${NC}" --title "${PASTEL_LIGHTGREEN}Complete${NC}" --msgbox "${WHITE}AUR package installation complete.${NC}" 8 40
