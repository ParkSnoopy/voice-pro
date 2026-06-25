#!/bin/bash
set -e

echo "========================================================================="
echo ""
echo "  ABUS Updater [Version 3.0]"
echo "  contact: abus.aikorea@gmail.com"
echo ""
echo "========================================================================="
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check for spaces in path
if [[ "$SCRIPT_DIR" =~ [[:space:]] ]]; then
    echo "This script relies on uv which can not be installed under a path with spaces."
    exit 1
fi

# Check uv is installed
if ! command -v uv &> /dev/null; then
    echo "ERROR: uv is not installed. Install it first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Setup paths
INSTALL_DIR="$SCRIPT_DIR/installer"
INSTALL_ENV_DIR="$INSTALL_DIR/env"
PYTHON_VERSION="3.12"

# Set temp/cache directories before any uv/pip command runs
export HOME="$INSTALL_DIR/home"
export TMPDIR="$INSTALL_DIR/tmp"
export TMP="$TMPDIR"
export TEMP="$TMPDIR"
export UV_CACHE_DIR="$INSTALL_DIR/uv-cache"
export PIP_CACHE_DIR="$INSTALL_DIR/uv-cache"
export UV_PYTHON_INSTALL_DIR="$INSTALL_DIR/uv-python"
export UV_TORCH_BACKEND=cpu
mkdir -p "$HOME" "$TMPDIR" "$UV_CACHE_DIR" "$UV_PYTHON_INSTALL_DIR"

# Check if venv exists
if [ ! -f "$INSTALL_ENV_DIR/bin/python" ]; then
    echo "Virtual environment not found. Please run start.sh first to set up the environment."
    exit 1
fi

# Recreate generated venv when the pinned Python runtime changes
PYTHON_BIN="$INSTALL_ENV_DIR/bin/python"
if ! "$PYTHON_BIN" -c "import sys, math, os; expected = tuple(map(int, '$PYTHON_VERSION'.split('.')[:2])); raise SystemExit(0 if sys.version_info[:2] == expected else 1)" 2>/dev/null; then
    echo "Virtual environment is incomplete, corrupted, or not Python $PYTHON_VERSION."
    echo "Removing environment and recreating..."
    rm -rf "$INSTALL_ENV_DIR"
    uv venv "$INSTALL_ENV_DIR" --python "$PYTHON_VERSION" || (echo "venv creation failed." && exit 1)
fi

# Environment isolation
export PYTHONNOUSERSITE=1
export PYTHONPATH=
export PYTHONHOME=
export VIRTUAL_ENV="$INSTALL_ENV_DIR"
export UV_PROJECT_ENVIRONMENT="$INSTALL_ENV_DIR"
# Keep all caches/temp inside the project dir; nothing leaks to ~, ~/.cache, ~/.config, ~/.local, or /tmp
export HOME="$INSTALL_DIR/home"
export TMPDIR="$INSTALL_DIR/tmp"
export XDG_CACHE_HOME="$INSTALL_DIR/xdg-cache"
export XDG_CONFIG_HOME="$INSTALL_DIR/xdg-config"
export XDG_DATA_HOME="$INSTALL_DIR/xdg-data"
export XDG_STATE_HOME="$INSTALL_DIR/xdg-state"
export GRADIO_TEMP_DIR="$INSTALL_DIR/gradio"
export STANZA_RESOURCES_DIR="$SCRIPT_DIR/model/stanza"
export HF_HOME="$SCRIPT_DIR/model/.hf_cache"
export HF_HUB_CACHE="$HF_HOME/hub"
export HUGGINGFACE_HUB_CACHE="$HF_HUB_CACHE"
export MODELSCOPE_CACHE="$SCRIPT_DIR/model/.modelscope_cache"
export UV_CACHE_DIR="$INSTALL_DIR/uv-cache"
export PIP_CACHE_DIR="$INSTALL_DIR/uv-cache"
export UV_PYTHON_INSTALL_DIR="$INSTALL_DIR/uv-python"
export MPLCONFIGDIR="$INSTALL_DIR/matplotlib"
export TORCH_HOME="$SCRIPT_DIR/model/.torch"
export TORCH_EXTENSIONS_DIR="$SCRIPT_DIR/model/.torch_extensions"
export CACHED_PATH_CACHE_DIR="$SCRIPT_DIR/model/.cached_path"
export NUMBA_CACHE_DIR="$INSTALL_DIR/numba-cache"
export TRITON_CACHE_DIR="$SCRIPT_DIR/model/.triton"
mkdir -p \
    "$HOME" "$TMPDIR" "$XDG_CACHE_HOME" "$XDG_CONFIG_HOME" "$XDG_DATA_HOME" \
    "$XDG_STATE_HOME" "$GRADIO_TEMP_DIR" "$STANZA_RESOURCES_DIR" \
    "$HF_HOME" "$HF_HUB_CACHE" "$MODELSCOPE_CACHE" "$UV_CACHE_DIR" \
    "$PIP_CACHE_DIR" "$UV_PYTHON_INSTALL_DIR" "$MPLCONFIGDIR" "$TORCH_HOME" \
    "$TORCH_EXTENSIONS_DIR" "$CACHED_PATH_CACHE_DIR" "$NUMBA_CACHE_DIR" \
    "$TRITON_CACHE_DIR"
source "$INSTALL_ENV_DIR/bin/activate"

cd "$SCRIPT_DIR"

export LOG_LEVEL=DEBUG
python start-abus.py voice --update

echo "Update process completed."
echo ""
