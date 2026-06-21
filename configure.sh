#!/bin/bash
set -e

echo "========================================================================="
echo ""
echo "  ABUS Configure [Version 3.0]"
echo "  contact: abus.aikorea@gmail.com"
echo ""
echo "========================================================================="
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if running as root (for package installation)
if [ "$EUID" -ne 0 ]; then
    echo "This script may need administrator privileges for some operations."
    echo "You may be prompted for your password."
    echo ""
fi

# Determine OS
echo "Linux detected"

# Detect package manager
if command -v apt-get &> /dev/null; then
    echo "Detected apt package manager"
    sudo apt-get update
    sudo apt-get install -y git ffmpeg build-essential
elif command -v yum &> /dev/null; then
    echo "Detected yum package manager"
    sudo yum install -y git ffmpeg gcc gcc-c++ make
elif command -v dnf &> /dev/null; then
    echo "Detected dnf package manager"
    sudo dnf install -y git ffmpeg gcc gcc-c++ make
elif command -v pacman &> /dev/null; then
    echo "Detected pacman package manager"
    sudo pacman -S --noconfirm git ffmpeg base-devel
else
    echo "Unsupported Linux distribution. Please install git and ffmpeg manually."
    exit 1
fi

# Check for NVIDIA GPU
if command -v nvidia-smi &> /dev/null; then
    echo "NVIDIA GPU detected. Please ensure CUDA toolkit is installed if needed."
    nvidia-smi
fi


echo ""
echo "ABUS configure.sh finished."
echo ""

