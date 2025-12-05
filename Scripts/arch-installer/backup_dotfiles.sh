#!/bin/bash
# backup_dotfiles.sh - Backup important dotfiles and directories.

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
BACKUP_DIR="assets/dotfiles"
HOME_DIR=~

# List of files and directories to backup
FILES_TO_BACKUP=(
    ".bashrc"
    ".bash_profile"
    ".gitconfig"
)

DIRS_TO_BACKUP=(
    ".config"
    ".themes"
    ".icons"
    ".fonts"
)

# --- Main ---
echo -e "${PASTEL_TEAL}Creating backup directory...${NC}"
mkdir -p "$BACKUP_DIR"

echo -e "${PASTEL_TEAL}Backing up files...${NC}"
for file in "${FILES_TO_BACKUP[@]}"; do
    if [ -f "$HOME_DIR/$file" ]; then
        echo -e "${PASTEL_LIGHTGREEN}Copying $file...${NC}"
        cp "$HOME_DIR/$file" "$BACKUP_DIR/"
    else
        echo -e "${PASTEL_YELLOW}Warning: $file not found, skipping.${NC}"
    fi
done

echo -e "${PASTEL_TEAL}Backing up directories...${NC}"
for dir in "${DIRS_TO_BACKUP[@]}"; do
    if [ -d "$HOME_DIR/$dir" ]; then
        echo -e "${PASTEL_LIGHTGREEN}Copying $dir...${NC}"
        cp -r "$HOME_DIR/$dir" "$BACKUP_DIR/"
    else
        echo -e "${PASTEL_YELLOW}Warning: $dir not found, skipping.${NC}"
    fi
done

echo -e "${PASTEL_LIGHTGREEN}Backup complete.${NC}"
echo -e "${WHITE}You can find the backed-up files in the '${BACKUP_DIR}' directory.${NC}"
echo -e "${WHITE}You may want to review the contents of this directory and remove any unnecessary or sensitive files.${NC}"
