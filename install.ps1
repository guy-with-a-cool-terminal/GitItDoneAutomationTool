Write-Host "🚀 Installing Git It Done (Windows)..."

# Step 1: Create venv if it doesn't exist
if (-Not (Test-Path ".venv")) {
    Write-Host "🔧 Creating virtual environment at .venv\"
    python -m venv .venv
}

# Step 2: Activate temporarily for install
. .\.venv\Scripts\Activate.ps1

# Step 3: Install dependencies
Write-Host "📦 Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Update shebang in gititdone.py to point to venv Python
$venvPython = Resolve-Path ".venv\Scripts\python.exe"
Write-Host "🔗 Updating shebang to use: $venvPython"

(Get-Content gititdone.py) | ForEach-Object {
    if ($_ -match "^#!") {
        "#!$venvPython"
    } else {
        $_
    }
} | Set-Content gititdone.py

# Step 5: Copy to a directory in PATH (optional: prompt user for preferred location)
$dest = "$env:USERPROFILE\gititdone.py"
Copy-Item gititdone.py $dest -Force

Write-Host "`n✅ Installed! You can now run the tool using:"
Write-Host "   python $dest"
Write-Host "`n💡 Tip: Add $env:USERPROFILE to your system PATH to use it globally as 'gititdone'"
