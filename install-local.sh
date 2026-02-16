#!/bin/bash

echo "🎯 Learning Agent - Local Edition Installer"
echo "==========================================="
echo "✨ No API keys required!"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    exit 1
fi

echo "✅ Python 3 found"

# Make executable
chmod +x learning-agent-local.py
echo "✅ Made script executable"

# Install
echo ""
echo "How would you like to install?"
echo "1) System-wide (requires sudo) - Recommended"
echo "2) User PATH only"
echo "3) Skip"
read -p "Choose (1/2/3): " choice

case $choice in
    1)
        sudo ln -sf "$(pwd)/learning-agent-local.py" /usr/local/bin/learning-agent-local
        echo "✅ Installed to /usr/local/bin/learning-agent-local"
        ;;
    2)
        AGENT_DIR="$(pwd)"
        if ! grep -q "learning-agent-local" ~/.bashrc; then
            echo "export PATH=\$PATH:$AGENT_DIR" >> ~/.bashrc
            echo "✅ Added to PATH. Run 'source ~/.bashrc'"
        fi
        ;;
    3)
        echo "⚠️  Skipped. Run './learning-agent-local.py' directly"
        ;;
esac

echo ""
echo "=================================="
echo "✨ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Run: learning-agent-local setup"
echo "2. Add your project directories"
echo "3. Run: learning-agent-local analyze --all"
echo ""
echo "🎉 No API keys needed!"
echo "=================================="
