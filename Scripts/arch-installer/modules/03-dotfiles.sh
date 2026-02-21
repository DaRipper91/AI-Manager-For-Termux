#!/bin/bash
# modules/03-dotfiles.sh - Restore dotfiles.

# --- Configuration ---
SOURCE_DIR="../assets/dotfiles"
DEST_DIR=~
DIALOG_HEIGHT=25
DIALOG_WIDTH=70

# --- Main ---
if [ ! -d "$SOURCE_DIR" ]; then
    dialog --backtitle "${PASTEL_TEAL}daripper os Installer${NC}" --title "${RED}Error${NC}" --msgbox "${WHITE}Dotfiles backup directory not found: $SOURCE_DIR${NC}" 8 40
    exit 1
fi

# Prepare the file list for the checklist dialog
cd "$SOURCE_DIR" || exit
files=(*)
cd - >/dev/null || exit

options=()
for file in "${files[@]}"; do
    options+=("$file" "" "on")
done

# Show the checklist dialog
exec 3>&1
selection=$(dialog \
    --separate-output \
    --backtitle "${PASTEL_TEAL}daripper os Installer${NC}" \
    --title "${PASTEL_PURPLE}Dotfile Selection${NC}" \
    --checklist "${WHITE}Select dotfiles and directories to restore:${NC}" \
    $DIALOG_HEIGHT $DIALOG_WIDTH 15 \
    "${options[@]}" \
    2>&1 1>&3)
exit_status=$?
exec 3>&-

if [ $exit_status -ne 0 ]; then
    exit
fi

if [ -z "$selection" ]; then
    dialog --backtitle "${PASTEL_TEAL}daripper os Installer${NC}" --title "${PASTEL_YELLOW}Warning${NC}" --msgbox "${WHITE}No items selected.${NC}" 8 40
    exit
fi

# Read selection into an array
mapfile -t selected_items <<< "$selection"

# Restore the selected items
for item_path in "${selected_items[@]}"; do
    source_path="$SOURCE_DIR/$item_path"
    dest_path="$DEST_DIR/$item_path"

    # Backup existing file/dir if it exists
    if [ -e "$dest_path" ]; then
        mv "$dest_path" "$dest_path.bak"
    fi

    # Copy the new file/dir
    cp -r "$source_path" "$dest_path"
done | dialog --progressbox "${WHITE}Restoring selected items...${NC}" 20 70

dialog --backtitle "${PASTEL_TEAL}daripper os Installer${NC}" --title "${PASTEL_LIGHTGREEN}Complete${NC}" --msgbox "${WHITE}Dotfile restoration complete. Existing files were backed up with a .bak extension.${NC}" 8 50
