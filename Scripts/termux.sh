# 1. Create the executable installer file
cat << 'EOF' > arch_x11_installer.sh
#!/data/data/com.termux/files/usr/bin/bash

# --- Termux Setup Script for Arch Linux and X11 Preparation ---
# This script prepares the Termux environment to host Arch Linux and enables
# graphical output using the Termux X11 app.

echo "🚀 Starting Termux initial setup..."

# 1. Add the Termux X11 repository
# This step is essential to ensure the Termux package manager (pkg) can find
# the necessary termux-x11-nightly package.
echo "🔄 Adding Termux X11 repository..."
pkg install -y termux-keyring
# The --tap option adds the X11 repository URL to the sources list
termux-change-repo --tap $PREFIX/etc/apt/sources.list.d/x11.list

echo "✅ X11 repository added."

# 2. Update and install core utilities in Termux
# proot-distro is used to install and manage the Arch Linux distribution.
# termux-x11-nightly provides the X server compatibility layer.
echo "⬇️ Updating packages and installing core utilities..."
pkg update -y
pkg upgrade -y
pkg install -y proot-distro git termux-x11-nightly

echo "✅ Termux base utilities and X11 support installed."

# 3. Install Arch Linux using proot-distro
echo "⬇️ Installing Arch Linux via proot-distro. This may take a while..."
proot-distro install archlinux

if [ $? -ne 0 ]; then
    echo "❌ Arch Linux installation failed. Exiting."
    exit 1
fi

echo "✅ Arch Linux base system installed."

# 4. Instruction for running the TUI and graphical apps
echo "🎉 Installation Phase 1 Complete! Arch Linux is installed inside Termux."
echo "------------------------------------"
echo "   NEXT STEPS (In Termux):"
echo "   1. Log into Arch: proot-distro login archlinux"
echo "   2. Install dialog: sudo pacman -S dialog"
echo "   3. Run your TUI installer: cd /path/to/installer && ./main.sh"
echo ""
echo "   To run a graphical app (e.g., Konsole) after installation:"
echo "      * Ensure you have the Termux X11 app downloaded and running."
echo '      * In the Arch terminal: export DISPLAY=:0.0'
echo '      * Run the app (e.g., Konsole): konsole &'
echo "------------------------------------"
EOF

# 2. Make the file executable
chmod +x arch_x11_installer.sh

echo "🎉 File 'arch_x11_installer.sh' created and ready to run!"
echo "To start the installation, simply run: ./arch_x11_installer.sh"
