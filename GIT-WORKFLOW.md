# Git Workflow

GitHub is the shared source of truth. Every computer is a local working copy.

## Before Working

## After Making Changes

```bash
git status
git add .
git commit -m "Describe the change"
git push
git status

The work is complete when Git reports that the branch is up to date with origin and the working tree is clean.

Multi-Machine Rule

Pull before work. Push before leaving the machine.

Do not manually copy project files between computers when GitHub can synchronize them.

If Push Is Rejected

Do not force push.

git pull

If Git reports a conflict, stop and resolve the conflict before pushing.

Never Use Routinely
git push --force

Force pushing can overwrite work from another machine.

Creating a New GitHub Repo

Preferred interface: Git Bash + GitHub CLI.

Verify GitHub CLI:

gh --version
gh auth status

From an existing local Git repo:

gh repo create rgrack-sys/<repo-name> --private --source=. --remote=origin --push

Use --public instead of --private when appropriate.

Prefer gh repo create instead of manually creating the repository in the GitHub website.

