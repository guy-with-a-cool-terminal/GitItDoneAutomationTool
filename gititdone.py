import os
import git
import argparse
import pyfiglet
from datetime import datetime
from git.exc import GitCommandError

def find_git_root(starting_path="."):
    """Find the root directory of the Git repository."""
    current_path = os.path.abspath(starting_path)
    while not os.path.exists(os.path.join(current_path, ".git")):
        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:  # Reached the root of the filesystem
            raise git.exc.InvalidGitRepositoryError("Not a git repository :(")
        current_path = parent_path
    return current_path

# Set the path to the root of the Git repository dynamically
try:
    repo_path = find_git_root()
    repo = git.Repo(repo_path)
except git.exc.InvalidGitRepositoryError as e:
    print(e)
    exit(1)

# get a default commit message with current timestamp
def get_commit_message(custom_message=None):
    if custom_message:
        return custom_message
    else:
        return f"Automated commit - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
# welcome banner and instructions
def print_welcome_message():
    banner = pyfiglet.figlet_format("Git  It  Done !")
    print(banner)
    print("Welcome to automate Git and rest a bit:) get it ?")
    print("This tool automates the process of committing and pushing changes to your git repository.")
    print("You can use it as follows:\n")
    print("Usage:")
    print("  python gititdone.py                - Commits all changes and pushes to the current branch with a default message.")
    print("  python gititdone.py --message \"Your custom commit message\" - Commits with your custom message.")
    print("  python gititdone.py --remote \"your-remote-name\"          - Pushes to a custom remote (default is 'origin').")
    print("  python gititdone.py --message \"Your custom commit message\" --remote \"your-remote-name\"")
    print("                               - Commits with a custom message and pushes to a custom remote.")
    print("\nMake sure your repository is clean and ready for commit before running this tool.")

# initialize git repo
try:
    repo = git.Repo(repo_path)
except git.exc.InvalidGitRepositoryError:
    print("Error: Not a git repository:( ")
    exit(1)
    
# parse arguments for custom commit messages and remote
parser = argparse.ArgumentParser(description='Automate Git commit and push.')
parser.add_argument('--message', type=str, help='Custom commit message')
parser.add_argument('--remote', type=str, default='origin', help='Remote repository name (default: origin)')
args = parser.parse_args()

# display welcome message/instructions
print_welcome_message()

# get commit message
commit_message = get_commit_message(args.message)

# add all changes
repo.git.add(A=True)

# commit changes
try:
    repo.index.commit(commit_message)
    print(f"\nChanges committed with message: '{commit_message}'")
except GitCommandError as e:
    print(f"Error during commit: {e}")
    exit(1)

# get current branch name
current_branch = repo.active_branch.name

# push changes to specified remote and current branch
try:
    origin = None
    for remote in repo.remotes:
        if remote.name == args.remote:
            origin = remote
            break
    
    if origin is None:
        print(f"Error: Remote '{args.remote}' not found.")
        exit(1)
    
    origin.push(refspec=f"{current_branch}:{current_branch}")
    print(f"\nChanges pushed to {args.remote}/{current_branch}")
except GitCommandError as e:
    print(f"Error during push: {e}")
    exit(1)
