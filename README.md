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
1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies**:
   Make sure you have Python installed. Then, install the required packages:
   ```bash
   pip install gitpython pyfiglet
   ```

---

## Usage

### Basic Command
To commit all changes and push to the current branch with a default commit message:
```bash
python gititdone.py
```

### With a Custom Commit Message
To commit with a custom message:
```bash
python gititdone.py --message "Your custom message here"
```

### Push to a Custom Remote
To push to a remote other than the default `origin`:
```bash
python gititdone.py --remote "your-remote-name"
```

### Combine Custom Message and Remote
You can specify both a custom commit message and a remote:
```bash
python gititdone.py --message "Your custom message here" --remote "your-remote-name"
```

---

## Example Output
```bash
(myenv) ┌─[batman@sudoer]─[~/Desktop/Brian/programming/gititdone]
└──╼ $ python3 gititdone.py 
  ____ _ _      ___ _      ____                     _ 
 / ___(_) |_   |_ _| |_   |  _ \  ___  _ __   ___  | |
| |  _| | __|   | || __|  | | | |/ _ \| '_ \ / _ \ | |
| |_| | | |_    | || |_   | |_| | (_) | | | |  __/ |_|
 \____|_|\__|  |___|\__|  |____/ \___/|_| |_|\___| (_)
                                                      

Welcome to automate Git and rest a bit:) get it ?
This tool automates the process of committing and pushing changes to your git repository.
You can use it as follows:

Usage:
  python gititdone.py                - Commits all changes and pushes to the current branch with a default message.
  python gititdone.py --message "Your custom commit message" - Commits with your custom message.
  python gititdone.py --remote "your-remote-name"          - Pushes to a custom remote (default is 'origin').
  python gititdone.py --message "Your custom commit message" --remote "your-remote-name"
                               - Commits with a custom message and pushes to a custom remote.

Make sure your repository is clean and ready for commit before running this tool.

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
