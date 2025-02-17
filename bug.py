import os
import git

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
        repo_path = os.getcwd() # Use current directory for new repo
        repo = git.Repo.init(repo_path)
        print("Initialized new repository in", repo_path)
        repo = git.Repo(repo_path) # Create git.Repo object *after* init
        print("Repository object created successfully.")
    else:
        exit(1)
except Exception as e: # Catch any other potential errors
    print(f"An unexpected error occurred: {e}")
    exit(1)

# Now you can use the 'repo' object
print("Successfully loaded or created repository. You can now interact with it.")
# Example:
# print(repo.git.status())