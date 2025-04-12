#!/bin/bash

set -e

echo "🚀 Installing Git It Done (Linux/macOS)..."

# create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "🔧 Creating virtual environment at .venv/"
    python3 -m venv .venv
fi

# activate venv
source .venv/bin/activate

# install dependencies
echo "📦 Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# update shebang
VENV_PYTHON=$(realpath .venv/bin/python)
echo "🔗 Updating shebang to use: $VENV_PYTHON"
sed -i "1s|^#!.*|#!$VENV_PYTHON|" gititdone.py

# make the script executable and copy it to /bin
chmod +x gititdone.py
sudo cp gititdone.py /usr/local/bin/gititdone

echo -e "\n✅ Installed! Now you can run 'gititdone' from anywhere 🎉"