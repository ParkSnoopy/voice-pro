#!/bin/bash
set -e

echo "========================================================================="
echo ""
echo "  ABUS Uninstaller [Version 3.0]"
echo "  contact: abus.aikorea@gmail.com"
echo ""
echo "========================================================================="
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Ask for confirmation
echo "This will remove the installer_files folder."
read -p "Do you want to continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled."
    exit 0
fi

# Terminate running Python processes (if any)
echo "Terminating running Python processes..."
pkill -f "python.*start-abus.py" || true
sleep 2

# Ask about system packages
echo ""
read -p "Would you like to remove system packages (ffmpeg, git, etc.)? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Removing system packages..."
    
    if command -v apt-get &> /dev/null; then
        sudo apt-get remove -y git ffmpeg build-essential || true
    elif command -v yum &> /dev/null; then
        sudo yum remove -y git ffmpeg gcc gcc-c++ make || true
    elif command -v dnf &> /dev/null; then
        sudo dnf remove -y git ffmpeg gcc gcc-c++ make || true
    elif command -v pacman &> /dev/null; then
        sudo pacman -R --noconfirm git ffmpeg base-devel || true
    fi
fi

# Remove installer_files folder
if [ -d "$SCRIPT_DIR/installer_files" ]; then
    echo "Deleting installer_files folder..."
    echo "Please wait a moment"
    rm -rf "$SCRIPT_DIR/installer_files"
    echo "installer_files folder deleted."
fi

echo ""
echo "ABUS uninstall.sh finished."
echo ""
echo "Note: The application folder itself was not deleted."
echo "To completely remove ABUS, delete this entire folder."


