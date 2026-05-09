Squash all commits that have not yet been pushed to the remote into a single commit.

Steps:
1. Run `git log --oneline origin/HEAD..HEAD` to identify unpushed commits. If there are none, tell the user and stop.
2. Review all the changes with `git diff origin/HEAD..HEAD --stat` and `git log --oneline origin/HEAD..HEAD` to understand what was done across all commits.
3. Soft-reset to `origin/HEAD` with `git reset --soft origin/HEAD` to collapse all unpushed commits into staged changes.
4. Write a single commit message that accurately describes the full set of changes — what was added, changed, or fixed, and why. Follow the commit style of the existing git log.
5. Commit with that message, including the standard co-author trailer.
6. Confirm success by showing the new single commit with `git log --oneline origin/HEAD..HEAD`.
