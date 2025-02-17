Here’s an **updated README** with instructions for making the script executable globally on **Linux** and **Windows**:  

---

# Git It Done: Automate Your Git Workflow! 🚀  

## Overview  
**Git It Done** is a Python-based tool designed to simplify your Git workflow. With just a single command, you can automate the process of committing and pushing your changes to a Git repository. Whether you're in the middle of a fast-paced development cycle or just want to save time, this tool has you covered.  

---

## Features  
- **Automated Commit Messages**: Generate default commit messages with a timestamp or provide your own.  
- **Push to Any Remote**: Specify the remote repository you want to push changes to (defaults to `origin`).  
- **Interactive Instructions**: Displays usage guidance for newcomers.  
- **Error Handling**: Detects invalid repositories, missing remotes, or issues during commits and pushes.  

---

## Installation  

### 1️⃣ Clone the Repository  
```bash
git clone <repository_url>
cd <repository_directory>
```

### 2️⃣ Install Dependencies  
Make sure you have Python installed. Then, install the required packages:  
```bash
pip install -r requirements.txt
```

---

## Making `gititdone.py` Executable from Anywhere  

### **🔹 Linux/macOS**  
1. **Ensure the script has a proper shebang** (edit `gititdone.py` and add this at the top if missing):  
   ```python
   #!/usr/bin/env python3
   ```
2. **Make the script executable**:  
   ```bash
   chmod +x gititdone.py
   ```
3. **Move it to `/usr/local/bin/` to make it globally accessible**:  
   ```bash
   sudo mv gititdone.py /usr/local/bin/gititdone
   ```
4. **Run it from anywhere**:  
   ```bash
   gititdone
   ```

**Using a Virtual Environment?**  
If `gititdone.py` relies on a virtual environment, replace the shebang (`#!/usr/bin/env python3`) with the full path to your environment’s Python:  
```python
#!/home/batman/Desktop/Brian/programming/gititdone/myenv/bin/python3
```

---

### **🔹 Windows**  
To run `gititdone.py` from anywhere on Windows:  

#### **Method 1: Add It to PATH**  
1. **Move the script to a fixed location**, e.g., `C:\git-tools\`.  
2. **Add that folder to the system `PATH`**:  
   - Search *Environment Variables* in the Windows search bar.  
   - Click *Edit the system environment variables* → *Environment Variables*.  
   - Under *System Variables*, find `Path`, click *Edit*, then *New*, and add `C:\git-tools\`.  
3. **Rename the file** to `gititdone.py` and now you can run:  
   ```powershell
   gititdone.py
   ```

#### **Method 2: Create a `.bat` Wrapper**  
1. **Create a `gititdone.bat` file** in `C:\git-tools\` with the following content:  
   ```bat
   @echo off
   python "C:\git-tools\gititdone.py" %*
   ```
2. **Move `gititdone.bat` to a folder in PATH** (like `C:\Windows\`).  
3. Now, you can just type:  
   ```powershell
   gititdone
   ```
   from anywhere! 🚀  

---

## Usage  

### Basic Command  
To commit all changes and push to the current branch with a default commit message:  
```bash
gititdone
```

### With a Custom Commit Message  
To commit with a custom message:  
```bash
gititdone --message "Your custom message here"
```

### Push to a Custom Remote  
To push to a remote other than the default `origin`:  
```bash
gititdone --remote "your-remote-name"
```

### Combine Custom Message and Remote  
You can specify both a custom commit message and a remote:  
```bash
gititdone --message "Your custom message here" --remote "your-remote-name"
```

---

## Example Output  
```bash
(myenv) ┌─[batman@sudoer]─[~/Desktop/Brian/programming/gititdone]
└──╼ $ gititdone
  ____ _ _      ___ _      ____                     _ 
 / ___(_) |_   |_ _| |_   |  _ \  ___  _ __   ___  | |
| |  _| | __|   | || __|  | | | |/ _ \| '_ \ / _ \ | |
| |_| | | |_    | || |_   | |_| | (_) | | | |  __/ |_|
 \____|_|\__|  |___|\__|  |____/ \___/|_| |_|\___| (_)
                                                      

Welcome to automate Git and rest a bit :) Get it?
This tool automates the process of committing and pushing changes to your git repository.
You can use it as follows:

Usage:
  gititdone                - Commits all changes and pushes to the current branch with a default message.
  gititdone --message "Your custom commit message" - Commits with your custom message.
  gititdone --remote "your-remote-name"          - Pushes to a custom remote (default is 'origin').
  gititdone --message "Your custom commit message" --remote "your-remote-name"
                               - Commits with a custom message and pushes to a custom remote.

Changes committed with message: 'Automated commit - 2025-01-25 11:21:23'
```

---

## Requirements  
- Python 3.6 or later  
- Git installed and configured  
- Python modules:  
  - `gitpython`  
  - `pyfiglet`  

---

## Error Handling  
- **Invalid Repository**: Displays an error if the script isn't run within a Git repository.  
- **Missing Remote**: Notifies you if the specified remote doesn't exist.  
- **Commit/Push Failures**: Provides detailed error messages if any Git operation fails.  

---

## License  
This project is open-source and available under the [MIT License](LICENSE).  

---

## Contributing  
Feel free to fork this repository, make changes, and submit a pull request! Your contributions are welcome. 💡  

---
