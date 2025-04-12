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
# Add or replace shebang
if head -n 1 gititdone.py | grep -q "^#!"; then
    sed -i "1s|^#!.*|#!$VENV_PYTHON|" gititdone.py
else
    sed -i "1i#!$VENV_PYTHON" gititdone.py
fi


# make the script executable and copy it to /bin
chmod +x gititdone.py
sudo cp gititdone.py /usr/local/bin/gititdone

echo -e "\n✅ Installed! Now you can run 'gititdone' from anywhere 🎉"