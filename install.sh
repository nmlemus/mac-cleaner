#!/bin/bash
# Quick installation script for Mac Cleaner

set -e

echo "🧹 Mac Cleaner Installation Script"
echo "=================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed."
    echo "Please install Python 3.8 or later from https://www.python.org/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Found Python $PYTHON_VERSION"

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Warning: This tool is designed for macOS only."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "Installing Mac Cleaner..."
echo ""

# Install in user mode
pip3 install --user -e .

echo ""
echo "✅ Installation complete!"
echo ""
echo "You can now run: mac-cleaner"
echo ""
echo "Tip: Add ~/.local/bin to your PATH if mac-cleaner is not found"
echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
echo ""
