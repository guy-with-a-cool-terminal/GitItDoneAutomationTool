if args.merge_from:
    try:
        from_branch = args.merge_from
        target_branch = args.merge_into if args.merge_into else current_branch

        print(f"Preparing to merge from '{from_branch}' into '{target_branch}'...")

        # Stash uncommitted changes to avoid interference during branch switches
        if repo.is_dirty(untracked_files=True):
            print("Uncommitted changes detected. Stashing them temporarily...")
            repo.git.stash('save', 'Auto-stash before merge')

        # Checkout target branch if not already on it
        if repo.active_branch.name != target_branch:
            print(f"Switching to target branch '{target_branch}'...")
            repo.git.checkout(target_branch)

        # Fetch and ensure both branches are up to date
        origin = repo.remotes[args.remote]
        origin.fetch()
        print("Fetched latest changes from remote.")

        repo.git.pull(args.remote, target_branch)
        print(f"Pulled latest changes into '{target_branch}'.")

        if from_branch not in repo.heads:
            print(f"Local branch '{from_branch}' not found. Checking out from remote...")
            repo.git.checkout('-b', from_branch, f'{args.remote}/{from_branch}')
        else:
            repo.git.checkout(from_branch)
            repo.git.pull(args.remote, from_branch)
            repo.git.checkout(target_branch)  # back to target branch

        # Merge
        repo.git.merge(from_branch)
        print(f"Successfully merged '{from_branch}' into '{target_branch}'.")

        # Push merged changes
        push_changes_to_remote(repo, args.remote, target_branch)

        # Restore stashed changes if any
        if repo.git.stash('list'):
            print("Restoring stashed changes...")
            repo.git.stash('pop')

        # Return to original working branch
        if target_branch != current_branch:
            repo.git.checkout(current_branch)
            print(f"Switched back to original branch '{current_branch}'.")

    except GitCommandError as e:
        print(f"❌ Merge failed: {e}")
        exit(1)
