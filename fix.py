# handle merge logic if --merge is used
if args.merge:
    try:
        # make sure we are working with the current branch
        current_branch = repo.active_branch.name
        print(f"Currently on branch: {current_branch}")

        # switch to target branch (main or master) for merging
        main_branch = repo.heads.main if 'main' in repo.heads else repo.heads.master
        if current_branch != main_branch.name:
            repo.git.checkout(main_branch)
            print(f"Switched to {main_branch} branch for merging.")

        # fetch latest changes from origin
        origin = repo.remotes.origin
        origin.fetch()
        print("Fetched latest changes from remote.")

        # pull latest changes from the target branch (main/master)
        repo.git.pull('origin', main_branch.name)
        print(f"Pulled latest changes from {main_branch.name}.")

        # merge the specified working branch (e.g., beta) into the target branch
        merge_branch = repo.heads[args.merge]  # Working branch, e.g., beta
        repo.git.merge(merge_branch)
        print(f"Successfully merged {args.merge} into {main_branch.name}.")

        # After merging, switch back to the working branch (e.g., beta)
        repo.git.checkout(current_branch)
        print(f"Switched back to {current_branch} branch.")

    except GitCommandError as e:
        print(f"Error during merge: {e}")
