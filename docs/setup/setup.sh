#!/bin/bash
# Setup script for LLM Simulation Survey System

echo "================================================"
echo "LLM Simulation Survey System - Setup"
echo "================================================"
echo ""

# Check Python
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Found: $PYTHON_VERSION"
else
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "Verifying installation..."
python3 verify_installation.py

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo "Setup Complete! 🎉"
    echo "================================================"
    echo ""
    echo "Next steps:"
    echo "1. Start LM Studio and load a model"
    echo "2. Run the app with: streamlit run app.py"
    echo "3. Check QUICKSTART.md for detailed instructions"
    echo ""
else
    echo ""
    echo "⚠️  Setup verification failed. Please check the errors above."
    exit 1
fi

