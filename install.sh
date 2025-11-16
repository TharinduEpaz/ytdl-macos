#!/bin/bash
# Installation script for YouTube Downloader CLI tool

echo "🚀 YouTube Downloader - Installation Script"
echo "==========================================="
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew is not installed."
    echo "Please install Homebrew first: https://brew.sh"
    echo ""
    echo "Run this command:"
    echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    exit 1
fi

echo "✅ Homebrew found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
echo ""

# Install yt-dlp
if ! command -v yt-dlp &> /dev/null; then
    echo "Installing yt-dlp..."
    brew install yt-dlp
else
    echo "✅ yt-dlp already installed"
fi

# Install ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "Installing ffmpeg..."
    brew install ffmpeg
else
    echo "✅ ffmpeg already installed"
fi

echo ""
echo "📝 Setting up ytdl command..."
echo ""

# Make the script executable
chmod +x ytdl.py

SCRIPT_PATH="$(pwd)/ytdl.py"

# Try to install to /usr/local/bin first
INSTALL_PATH="/usr/local/bin/ytdl"

# Check if /usr/local/bin exists, create if not
if [ ! -d "/usr/local/bin" ]; then
    echo "Creating /usr/local/bin directory..."
    sudo mkdir -p /usr/local/bin
fi

# Remove existing installation if present
if [ -L "$INSTALL_PATH" ] || [ -f "$INSTALL_PATH" ]; then
    echo "Removing existing ytdl command..."
    sudo rm "$INSTALL_PATH"
fi

# Try to create symlink with sudo
echo "Creating ytdl command (may require password)..."
if sudo ln -s "$SCRIPT_PATH" "$INSTALL_PATH" 2>/dev/null; then
    echo "✅ Installed to /usr/local/bin/ytdl"
    INSTALLED=true
else
    echo "⚠️  Could not install to /usr/local/bin"
    echo "Installing to ~/.local/bin instead..."
    
    # Fallback to ~/.local/bin
    mkdir -p "$HOME/.local/bin"
    INSTALL_PATH="$HOME/.local/bin/ytdl"
    
    if [ -L "$INSTALL_PATH" ] || [ -f "$INSTALL_PATH" ]; then
        rm "$INSTALL_PATH"
    fi
    
    ln -s "$SCRIPT_PATH" "$INSTALL_PATH"
    
    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo ""
        echo "⚠️  Add ~/.local/bin to your PATH by adding this line to ~/.zshrc:"
        echo "   export PATH=\"\$HOME/.local/bin:\$PATH\""
        echo ""
        echo "Then run: source ~/.zshrc"
    fi
    
    INSTALLED=true
fi

if [ "$INSTALLED" = true ]; then
    echo ""
    echo "✅ Installation complete!"
    echo ""
    echo "Usage:"
    echo "  ytdl \"https://www.youtube.com/watch?v=VIDEO_ID\""
    echo "  ytdl \"URL\" -q 720p -o ~/Downloads"
    echo "  ytdl \"URL\" --audio-only"
    echo "  ytdl \"URL\" --list-formats"
    echo ""
    echo "Run 'ytdl --help' for more options"
    echo ""
fi
