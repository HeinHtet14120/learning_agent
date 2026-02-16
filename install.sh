#!/bin/bash

echo "🎯 Learning Agent - Quick Installer"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install anthropic requests --break-system-packages

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"

# Make script executable
chmod +x learning-agent.py
echo "✅ Made script executable"

# Ask user how they want to install
echo ""
echo "How would you like to install the command?"
echo "1) System-wide (requires sudo) - Recommended"
echo "2) User PATH only"
echo "3) Skip installation (manual setup)"
read -p "Choose option (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "Installing system-wide to /usr/local/bin..."
        sudo ln -sf "$(pwd)/learning-agent.py" /usr/local/bin/learning-agent
        if [ $? -eq 0 ]; then
            echo "✅ Installed to /usr/local/bin/learning-agent"
        else
            echo "❌ Installation failed"
            exit 1
        fi
        ;;
    2)
        echo ""
        echo "Adding to PATH in ~/.bashrc..."
        AGENT_DIR="$(pwd)"
        if ! grep -q "learning-agent" ~/.bashrc; then
            echo "export PATH=\$PATH:$AGENT_DIR" >> ~/.bashrc
            echo "✅ Added to PATH. Run 'source ~/.bashrc' to apply"
        else
            echo "⚠️  Already in PATH"
        fi
        ;;
    3)
        echo "⚠️  Skipping installation. Run './learning-agent.py' directly"
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "=================================="
echo "✨ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Run: learning-agent setup"
echo "2. Follow the prompts to configure Notion"
echo "3. Run: learning-agent analyze"
echo ""
echo "📖 For detailed guide, see: INSTALLATION.md"
echo "=================================="
