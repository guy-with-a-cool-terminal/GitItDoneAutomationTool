# Get the current branch name
current_branch = repo.active_branch.name

# Push changes to remote and ensure the branch is pushed to the correct remote
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

        # If branch doesn't exist, set upstream and push
        if not remote_branch_exists:
            print(f"Remote branch '{branch_name}' does not exist. Publishing it now.")
            repo.git.push("--set-upstream", remote_name, branch_name)
            print(f"Branch '{branch_name}' is now tracked with remote '{remote_name}'.")
        else:
            # Sync the branch if it exists remotely
            local_commit = repo.commit(branch_name)
            remote_commit = repo.commit(remote_ref)
            if local_commit.hexsha != remote_commit.hexsha:
                print(f"Local branch '{branch_name}' is out of sync with remote '{remote_name}'.")
                print("Pulling latest changes to sync...")
                repo.git.pull(remote_name, branch_name)
                print(f"Successfully pulled latest changes for branch '{branch_name}'.")

        # Finally push to the remote branch
        repo.git.push(remote_name, branch_name)
        print(f"Changes successfully pushed to {remote_name}/{branch_name}.")

    except GitCommandError as e:
        print(f"Error during push operation: {e}")
        exit(1)

# If there is a --merge argument, handle merge logic first
if args.merge:
    try:
        # Make sure we are working with the current branch
        current_branch = repo.active_branch.name
        print(f"Currently on branch: {current_branch}")

        # Switch to the main branch for merge operation
        main_branch = repo.heads.main if 'main' in repo.heads else repo.heads.master
        repo.git.checkout(main_branch)
        print(f"Switched to {main_branch} branch.")

        # Fetch latest changes from the origin
        origin = repo.remotes.origin
        origin.fetch()
        print("Fetched latest changes from remote.")

        # Pull the latest changes from the current branch
        repo.git.pull('origin', current_branch)
        print(f"Pulled latest changes from {current_branch}.")

        # Merge the specified branch
        merge_branch = repo.heads[args.merge]
        repo.git.merge(merge_branch)
        print(f"Successfully merged {args.merge} into {current_branch}.")
    except GitCommandError as e:
        print(f"Error during merge: {e}")
        exit(1)

# Commit all changes and push them to the current branch
repo.git.add(A=True)

# Commit changes with custom or default message
commit_message = get_commit_message(args.message)

try:
    repo.index.commit(commit_message)
    print(f"\nChanges committed with message: '{commit_message}'")
except GitCommandError as e:
    print(f"Error during commit: {e}")
    exit(1)

# Push the current branch to the remote
push_changes_to_remote(repo, args.remote, current_branch)
