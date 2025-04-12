        # return to original working branch
        if target_branch != current_branch:
            repo.git.checkout(current_branch)
            print(f"Switched back to {current_branch} branch.")

        # ✅ Exit here to prevent duplicate commit/push
        exit(0)
