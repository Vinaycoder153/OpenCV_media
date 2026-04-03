#!/bin/bash
# Quick Start Setup Script for Google Gemini API Integration
# This script helps you set up Google Gemini API in minutes

set -e

echo "=================================================="
echo "  Google Gemini API - Quick Start Setup"
echo "=================================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔄 Activating virtual environment..."
source .venv/bin/activate || . .venv/Scripts/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip -q

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "🔐 Setting up environment configuration..."
    cat > .env << 'EOF'
# Google Gemini API Configuration
# Get your API key from: https://aistudio.google.com/app/apikeys

GOOGLE_API_KEY=YOUR_API_KEY_HERE
GOOGLE_MODEL=gemini-1.5-flash
GOOGLE_TEMPERATURE=0.7
EOF
    echo "✓ Created .env file (update with your API key)"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "=================================================="
echo "  ✅ Setup Complete!"
echo "=================================================="
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Get your Google API key:"
echo "   👉 https://aistudio.google.com/app/apikeys"
echo ""
echo "2. Update .env file with your API key:"
echo "   nano .env"
echo "   (or open .env with your favorite editor)"
echo ""
echo "3. Source the environment (or it's auto-loaded):"
echo "   source .env"
echo ""
echo "4. Run the application:"
echo "   python main.py"
echo ""
echo "📚 For more details, see GEMINI_SETUP.md"
echo ""
