Alright, here's your updated `README.md` with the **new automatic setup using virtual environments**, complete with platform-specific setup scripts (`install.sh` for Linux/macOS and `install.ps1` for Windows). I’ve preserved everything else as-is and swapped out the manual setup instructions with the new auto-setup.

---

# **Git It Done: Automate Your Git Workflow!** 🚀  

## **Overview**  
**Git It Done** is a Python-based tool designed to simplify your Git workflow. With just a single command, you can automate the process of committing and pushing your changes to a Git repository. Whether you're in the middle of a fast-paced development cycle or just want to save time, this tool has you covered.  

---

## **Features**  
✅ **Automated Commit Messages**: Generate default commit messages with a timestamp or provide your own.  
✅ **Push to Any Remote**: Specify the remote repository you want to push changes to (defaults to `origin`).  
✅ **Interactive Instructions**: Displays usage guidance for newcomers.  
✅ **Error Handling**: Detects invalid repositories, missing remotes, or issues during commits and pushes.  

---

## **Installation**  

### **1️⃣ Clone the Repository**  
```bash
git clone <repository_url>
cd <repository_directory>
```

### **2️⃣ Automatic Setup with Virtual Environment**  

To get started with zero configuration, just run the install script for your platform:

#### 🔹 **Linux/macOS**
```bash
bash install.sh
```

This will:
- Create a virtual environment in `.venv/`
- Install all required dependencies
- Update the shebang in `gititdone.py` to point to the venv’s Python
- Make `gititdone` globally accessible from the terminal

#### 🔹 **Windows (PowerShell)**
```powershell
./install.ps1
```

This will:
- Create a virtual environment in `.venv\`
- Install all dependencies
- Patch the script’s shebang or execution path
- Add an alias `gititdone` to your PowerShell profile for global use

> ⚠️ Note: Ensure PowerShell execution policy allows script execution (`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`).

---

## **Usage**  

### **Basic Command**  
To commit all changes and push to the current branch with a default commit message:  
```bash
gititdone
```

### **With a Custom Commit Message**  
To commit with a custom message:  
```bash
gititdone --message "Your custom message here"
```

### **Push to a Custom Remote**  
To push to a remote other than the default `origin`:  
```bash
gititdone --remote "your-remote-name"
```

### **Combine Custom Message and Remote**  
You can specify both a custom commit message and a remote:  
```bash
gititdone --message "Your custom message here" --remote "your-remote-name"
```

---

## **Example Output**  
```bash
(.venv) ┌─[batman@sudoer]─[~/Desktop/Brian/programming/gititdone]
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

## **Requirements**  
- Python 3.6 or later  
- Git installed and configured  
- Python modules (installed automatically):  
  - `gitpython`  
  - `pyfiglet`  

---

## **Error Handling**  
- **Invalid Repository**: Displays an error if the script isn't run within a Git repository.  
- **Missing Remote**: Notifies you if the specified remote doesn't exist.  
- **Commit/Push Failures**: Provides detailed error messages if any Git operation fails.  

---

## **License**  
This project is open-source and available under the [MIT License](LICENSE).  

---

## **Contributing**  
Feel free to fork this repository, make changes, and submit a pull request! Your contributions are welcome. 💡  

---