import os
import git
import argparse
import pyfiglet
from datetime import datetime
from git.exc import GitCommandError

def find_git_root(starting_path="."):
    current_path = os.path.abspath(starting_path)
    while not os.path.exists(os.path.join(current_path, ".git")):
        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:
            raise git.exc.InvalidGitRepositoryError("Not a git repository :(")
        current_path = parent_path
    return current_path

try:
    repo_path = find_git_root()
    repo = git.Repo(repo_path)
except git.exc.InvalidGitRepositoryError as e:
    print(e)
    user_input = input("Would you like to initialize a new git repository here? (y/n): ")
    if user_input.lower() == 'y':
        repo_path = os.getcwd()
        repo = git.Repo.init(repo_path)
        print("Initialized new repository in:", repo_path)
    else:
        exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit(1)

def get_commit_message(custom_message=None):
    return custom_message or f"Automated commit - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

def print_welcome_message():
    banner = pyfiglet.figlet_format("Git  It  Done !")
    print(banner)
    print("Welcome to automate Git and rest a bit :) Get it?\n")
    print("Usage:")
    print("  python gititdone.py")
    print("  python gititdone.py --message \"Your message\"")
    print("  python gititdone.py --remote \"your-remote-name\"")
    print("  python gititdone.py --merge-from <branch> [--merge-into <branch>]\n")
    print("Make sure your repository is clean and ready for commit before running this tool.")

parser = argparse.ArgumentParser(description='Automate Git commit and push.')
parser.add_argument('--message', type=str, help='Custom commit message')
parser.add_argument('--remote', type=str, default='origin', help='Remote name (default: origin)')
parser.add_argument('--merge-from', type=str, help='Branch to merge from')
parser.add_argument('--merge-into', type=str, help='Branch to merge into (optional)')
args = parser.parse_args()

print_welcome_message()
current_branch = repo.active_branch.name

def handle_protected_branch_push(repo, remote_name, target_branch):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    temp_branch_name = f"merge-{target_branch}-auto-{timestamp}"
    print(f"Creating temporary branch '{temp_branch_name}' for pull request...")

    repo.git.checkout('-b', temp_branch_name)

    try:
        repo.git.push(remote_name, temp_branch_name)
        print(f"Branch '{temp_branch_name}' pushed to remote '{remote_name}'.")

        remote_url = repo.remotes[remote_name].url
        if remote_url.endswith(".git"):
            remote_url = remote_url[:-4]
        if remote_url.startswith("git@github.com:"):
            remote_url = remote_url.replace("git@github.com:", "https://github.com/")

        pr_url = f"{remote_url}/compare/{target_branch}...{temp_branch_name}"
        print("\n🔔 ACTION NEEDED:")
        print(f"➡️  Please create a pull request: {pr_url}\n")

    except GitCommandError as push_error:
        print(f"Failed to push temporary branch: {push_error}")
        exit(1)
    finally:
        repo.git.checkout(target_branch)

def push_changes_to_remote(repo, remote_name, branch_name):
    try:
        origin = next((r for r in repo.remotes if r.name == remote_name), None)
        if not origin:
            print(f"Remote '{remote_name}' not found.")
            exit(1)

        origin.fetch()
        print(f"Fetched latest updates from remote '{remote_name}'.")

        remote_ref = f"{remote_name}/{branch_name}"
        remote_branch_exists = remote_ref in [ref.name for ref in origin.refs]

        if not remote_branch_exists:
            print(f"Remote branch '{branch_name}' does not exist. Publishing it now.")
            repo.git.push("--set-upstream", remote_name, branch_name)
            print(f"Branch '{branch_name}' is now tracked with remote '{remote_name}'.")
        else:
            local_commit = repo.commit(branch_name)
            remote_commit = repo.commit(remote_ref)

            if local_commit.hexsha != remote_commit.hexsha:
                print(f"Local branch '{branch_name}' is out of sync. Pulling latest...")
                repo.git.pull(remote_name, branch_name)
                print(f"Pulled latest changes for branch '{branch_name}'.")

        repo.git.push(remote_name, branch_name)
        print(f"Changes pushed to {remote_name}/{branch_name}.")

    except GitCommandError as e:
        if "push declined due to repository rule violations" in str(e):
            print("Push blocked due to branch protection rules.")
            handle_protected_branch_push(repo, remote_name, branch_name)
        else:
            print(f"Push error: {e}")
            exit(1)

# Handle merging branches
if args.merge_from:
    from_branch = args.merge_from
    target_branch = args.merge_into or current_branch
    print(f"Currently on branch: {current_branch}")
    print(f"Merging from '{from_branch}' into '{target_branch}'...")

    if repo.is_dirty(untracked_files=True):
        print("Stashing uncommitted changes...")
        repo.git.stash('save', 'Auto-stash before merge')

    if repo.active_branch.name != target_branch:
        repo.git.checkout(target_branch)

    origin = repo.remotes[args.remote]
    origin.fetch()
    repo.git.pull(args.remote, target_branch)

    if from_branch not in repo.heads:
        print(f"Local '{from_branch}' not found. Creating from remote...")
        repo.git.checkout('-b', from_branch, f'{args.remote}/{from_branch}')
    else:
        repo.git.checkout(from_branch)
        repo.git.pull(args.remote, from_branch)
        repo.git.checkout(target_branch)

    try:
        repo.git.merge(from_branch)
        print(f"Merged '{from_branch}' into '{target_branch}'.")
        push_changes_to_remote(repo, args.remote, target_branch)

        if repo.git.stash('list'):
            print("Restoring stashed changes...")
            repo.git.stash('pop')

        if target_branch != current_branch:
            repo.git.checkout(current_branch)
            print(f"Switched back to {current_branch}.")

    except GitCommandError as e:
        print(f"Merge error: {e}")
        exit(1)

    exit(0)

# If no merge, proceed with commit + push
repo.git.add(A=True)
commit_message = get_commit_message(args.message)

try:
    repo.index.commit(commit_message)
    print(f"Committed changes: '{commit_message}'")
except Exception as e:
    print(f"Commit failed: {e}")
    exit(1)

push_changes_to_remote(repo, args.remote, current_branch)
