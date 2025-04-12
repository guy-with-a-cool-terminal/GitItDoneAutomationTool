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
    # prompt the user to initialize a repo if not found
    user_input = input("Would you like to initialize a new git repository here? (y/n): ")
    if user_input.lower() == 'y':
        repo_path = os.getcwd()  # use current directory for new repo
        repo = git.Repo.init(repo_path)
        print("initialized new repository in:", repo_path)
        repo = git.Repo(repo_path)
        print("repository object created successfully")
    else:
        exit(1)

except Exception as e:
    print(f"an unexpected error occurred: {e}")
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
    print("  python gititdone.py --merge-from <branch> [--merge-into <branch>] - Merges from one branch into the current or specified branch.")
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
parser.add_argument('--merge-from', type=str, help='Branch to merge from')
parser.add_argument('--merge-into', type=str, help='Branch to merge into (optional, defaults to current branch)')
args = parser.parse_args()

# display welcome message/instructions
print_welcome_message()

#  Get the current branch name
current_branch = repo.active_branch.name
def push_changes_to_remote(repo, remote_name, branch_name):
    try:
        # Find the remote
        origin = next((remote for remote in repo.remotes if remote.name == remote_name), None)
        if origin is None:
            print(f"Error: Remote '{remote_name}' not found.")
            exit(1)

        # Fetch the latest from remote
        origin.fetch()
        print(f"Fetched latest updates from remote '{remote_name}'.")

        # Check if the branch exists on the remote
        remote_ref = f"{remote_name}/{branch_name}"
        remote_branch_exists = remote_ref in [ref.name for ref in origin.refs]

        # Publish the branch if it doesn't exist on the remote
        if not remote_branch_exists:
            print(f"Remote branch '{branch_name}' does not exist. Publishing it now.")
            repo.git.push("--set-upstream", remote_name, branch_name)
            print(f"Branch '{branch_name}' is now tracked with remote '{remote_name}'.")
        else:
            # Sync the branch if remote branch exists
            local_commit = repo.commit(branch_name)
            remote_commit = repo.commit(remote_ref)

            if local_commit.hexsha != remote_commit.hexsha:
                print(f"Local branch '{branch_name}' is out of sync with remote '{remote_name}'.")
                print("Pulling latest changes to sync...")
                repo.git.pull(remote_name, branch_name)
                print(f"Successfully pulled latest changes for branch '{branch_name}'.")

        # Push local changes to remote
        repo.git.push(remote_name, branch_name)
        print(f"Changes successfully pushed to {remote_name}/{branch_name}.")

    except GitCommandError as e:
        print(f"Error during push operation: {e}")
        exit(1)

# handle merge logic if --merge-from is used
if args.merge_from:
    try:
        # make sure we are working with the current branch
        from_branch = args.merge_from
        target_branch = args.merge_into if args.merge_into else current_branch
        print(f"currently on branch: {current_branch}")
        print(f"Preparing to merge from '{from_branch}' into '{target_branch}'...")
        
        # stash uncommitted changes
        if repo.is_dirty(untracked_files=True):
            print("Uncommitted changes detected. Stashing them temporarily...")
            repo.git.stash('save','Auto-stash before merge')

        # checkout target branch if not already on it
        if repo.active_branch.name != target_branch:
            print(f"Switching to target branch '{target_branch}'...")
            repo.git.checkout(target_branch)
        
        # fetch and ensure both branches are up to date
        origin = repo.remotes[args.remote]
        origin.fetch()
        print("Fetched latest changes from remote.")
        
        repo.git.pull(args.remote,target_branch)
        print(f"Pulled latest changes into '{target_branch}'.")

        if from_branch not in repo.heads:
            print(f"Local branch '{from_branch}' not found. Checking out from remote...")
            repo.git.checkout('-b', from_branch, f'{args.remote}/{from_branch}')
        else:
            repo.git.checkout(from_branch)
            repo.git.pull(args.remote, from_branch)
            repo.git.checkout(target_branch)  # back to target branch

        # merge   
        repo.git.merge(from_branch)
        print(f"Successfully merged '{from_branch}' into '{target_branch}'.")
        
        # Push the main/master branch after merging
        push_changes_to_remote(repo, args.remote, target_branch)
        print(f"Pushed merged changes to {args.remote}/{target_branch}.")
        
        # restore stahed changes if any
        if repo.git.stash('list'):
            print("Restoring stashed changes...")
            repo.git.stash('pop')

        # return to original working branch
        if target_branch != current_branch:
            repo.git.checkout(current_branch)
            print(f"Switched back to {current_branch} branch.")
        
        exit(0)

    except GitCommandError as e:
        print(f"Error during merge: {e}")
        exit(1)

repo.git.add(A=True)

# commit changes
commit_message = get_commit_message(args.message)
try:
    repo.index.commit(commit_message)
    print(f"\nChanges committed with message: '{commit_message}'")
except GitCommandError as e:
    print(f"error during commit: {e}")
    exit(1)

# push current branch to remote
push_changes_to_remote(repo,args.remote,current_branch)
