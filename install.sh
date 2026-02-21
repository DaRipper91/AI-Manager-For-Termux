#!/bin/bash

# install.sh - Bootstrap for the Universal Installer

echo "Checking dependencies..."

if [ -n "$TERMUX_VERSION" ] || [[ "$PREFIX" == *"com.termux"* ]]; then
    echo "Detected Termux environment."
    pkg update -y
    pkg install -y python dialog
elif [ -f "/etc/arch-release" ] || command -v pacman &> /dev/null; then
    echo "Detected Arch-based environment."
    if command -v sudo &> /dev/null; then
        sudo pacman -S --needed --noconfirm python dialog
    else
        pacman -S --needed --noconfirm python dialog
    fi
else
    echo "Unknown environment. Please ensure 'python' and 'dialog' are installed manually."
fi

# Run the python script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/Scripts/universal_installer.py"
