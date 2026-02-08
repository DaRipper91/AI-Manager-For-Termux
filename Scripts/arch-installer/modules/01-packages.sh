#!/bin/bash
# modules/01-packages.sh - Install packages from official repositories.

# --- Configuration ---
SCRIPT_DIR=$(dirname "$(realpath "$0")")
DATA_FILE="$SCRIPT_DIR/../data/packages.list"
DIALOG_HEIGHT=25
DIALOG_WIDTH=70

# --- Main ---
if [ ! -f "$DATA_FILE" ]; then
    dialog --backtitle "${PASTEL_TEAL}daripper os Installer${NC}" --title "${RED}Error${NC}" --msgbox "${WHITE}Package list file not found: $DATA_FILE${NC}" 8 40
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
    --backtitle "${PASTEL_TEAL}daripper os Installer${NC}" \
    --title "${PASTEL_PURPLE}Package Selection${NC}" \
    --checklist "${WHITE}Select packages to install:${NC}" \
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

# Install the selected packages
dialog --backtitle "${PASTEL_TEAL}daripper os Installer${NC}" --title "${PASTEL_LIGHTBLUE}Installation${NC}" --infobox "${WHITE}Installing selected packages...${NC}" 5 40
eval "sudo pacman -S --noconfirm --needed $selection" | dialog --progressbox "${WHITE}Installing packages...${NC}" 20 70

dialog --backtitle "${PASTEL_TEAL}daripper os Installer${NC}" --title "${PASTEL_LIGHTGREEN}Complete${NC}" --msgbox "${WHITE}Package installation complete.${NC}" 8 40
