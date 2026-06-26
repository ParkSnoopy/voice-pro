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
    sudo apt-get install -y git ffmpeg build-essential pkg-config libopenblas-dev libomp-dev libnuma-dev libvulkan-dev mesa-vulkan-drivers vulkan-tools glslang-tools libshaderc-dev spirv-tools
elif command -v yum &> /dev/null; then
    echo "Detected yum package manager"
    sudo yum install -y git ffmpeg gcc gcc-c++ make pkgconf-pkg-config openblas-devel libomp-devel numactl-devel vulkan-headers vulkan-loader-devel mesa-vulkan-drivers vulkan-tools glslang shaderc-devel spirv-tools
elif command -v dnf &> /dev/null; then
    echo "Detected dnf package manager"
    sudo dnf install -y git ffmpeg gcc gcc-c++ make pkgconf-pkg-config openblas-devel libomp-devel numactl-devel vulkan-headers vulkan-loader-devel mesa-vulkan-drivers vulkan-tools glslang shaderc-devel spirv-tools
elif command -v pacman &> /dev/null; then
    echo "Detected pacman package manager"
    sudo pacman -S --noconfirm git ffmpeg base-devel pkgconf openblas libomp numactl vulkan-headers vulkan-icd-loader mesa-vulkan-drivers vulkan-tools glslang shaderc spirv-tools
else
    echo "Unsupported Linux distribution. Please install git, ffmpeg, build tools, OpenBLAS, OpenMP, NUMA, Vulkan, glslang, shaderc, and SPIR-V tools manually."
    exit 1
fi



echo ""
echo "ABUS configure.sh finished."
echo ""

