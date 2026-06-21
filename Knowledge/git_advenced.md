# Git Advanced Complete Reference


---

# CHAPTER 1: GIT INTERNALS


## Remarks

Git is a distributed version control system created by Linus Torvalds in 2005 for Linux kernel development. It tracks content changes, not files, using a DAG (Directed Acyclic Graph) of commits. Understanding Git's internal model prevents 99% of "I messed up my repo" problems.

Key concepts: **Commits** (snapshots, not diffs), **Branches** (lightweight pointers to commits), **HEAD** (pointer to current branch/commit), **Index/Staging Area** (next commit preview), **Objects** (blobs, trees, commits, tags), **Refs** (branch names, tags, HEAD), **Remotes** (named URLs to other repos).

Used by: every professional software project. Git fluency is as fundamental as typing.

Tools: **git CLI** (primary), **GitHub/GitLab/Bitbucket** (hosting), **lazygit** (TUI), **GitKraken/Fork/SourceTree** (GUI), **git-delta** (better diffs), **pre-commit** (hooks framework), **conventional-commits** (commit message standard).


## Git Object Model

```
FOUR OBJECT TYPES:

BLOB    — file content (no name, just bytes + SHA-1 hash)
TREE    — directory listing (names → blobs/subtrees)
COMMIT  — snapshot: points to root tree + parent(s) + metadata
TAG     — annotated pointer to a commit (with message, author)

Everything is content-addressed by SHA-1 hash.

Example:
  commit a1b2c3d
    ├── tree 4e5f6a7
    │   ├── blob 8b9c0d1  README.md
    │   ├── blob 2e3f4a5  package.json
    │   └── tree 6c7d8e9  src/
    │       ├── blob f0a1b2c  index.ts
    │       └── blob 3d4e5f6  utils.ts
    ├── parent: commit 7a8b9c0
    ├── author: Alice <alice@example.com>
    ├── date: 2026-06-10 14:30:00
    └── message: "Add user authentication"

# Inspect objects
git cat-file -t a1b2c3d           # Type: commit
git cat-file -p a1b2c3d           # Pretty-print content
git cat-file -p 4e5f6a7           # Tree listing
git ls-tree HEAD                  # Root tree of current commit
git rev-parse HEAD                # Full SHA of HEAD
```


## The Three Areas

```
WORKING DIRECTORY        STAGING AREA (INDEX)        REPOSITORY (.git)
(your files on disk)     (next commit preview)       (committed history)

    edit files
        │
        ├── git add ──────────►
        │                           │
        │                           ├── git commit ──────────►
        │                           │                           │
        ◄── git restore ───────────┘                           │
        │                                                       │
        ◄── git checkout / git restore --staged ───────────────┘

# See what's where
git status                   # Overview
git diff                     # Working dir vs staging
git diff --staged            # Staging vs last commit (what will commit)
git diff HEAD                # Working dir vs last commit

# Stash (temporary save, clean working dir)
git stash                    # Save changes, clean tree
git stash pop                # Restore most recent stash
git stash list               # All stashes
git stash show -p stash@{0}  # Show diff of specific stash
git stash drop stash@{0}     # Delete specific
git stash push -m "wip auth" # Named stash
git stash push -- file.txt   # Stash specific file
```


---

# CHAPTER 2: BRANCHING STRATEGIES


## Branch Basics

```bash
# Create branch
git branch feature/login
git checkout -b feature/login          # Create + switch (old way)
git switch -c feature/login            # Create + switch (modern)

# List branches
git branch                             # Local
git branch -r                          # Remote
git branch -a                          # All
git branch -v                          # With last commit
git branch --merged                    # Merged into current
git branch --no-merged                 # Not yet merged

# Switch
git switch main
git checkout main                      # Old way

# Rename
git branch -m old-name new-name
git branch -m new-name                 # Rename current

# Delete
git branch -d feature/login           # Safe delete (only if merged)
git branch -D feature/login           # Force delete
git push origin --delete feature/login # Delete remote branch

# Track remote branch
git branch --set-upstream-to=origin/main main
git checkout --track origin/feature    # Create local tracking branch
```


## Git Flow

```
BRANCHES:
  main        — production code, always stable
  develop     — integration branch, next release
  feature/*   — new features (from develop)
  release/*   — release prep (from develop → main)
  hotfix/*    — urgent fixes (from main → main + develop)

WORKFLOW:
  1. Create feature branch from develop
     git checkout -b feature/login develop

  2. Work on feature (multiple commits)
     git commit -m "Add login form"
     git commit -m "Add validation"

  3. Finish feature: merge back to develop
     git checkout develop
     git merge --no-ff feature/login
     git branch -d feature/login

  4. Create release branch
     git checkout -b release/1.0 develop
     # Bug fixes only, no new features
     git commit -m "Fix login edge case"

  5. Finish release: merge to main AND develop
     git checkout main
     git merge --no-ff release/1.0
     git tag -a v1.0 -m "Release 1.0"
     git checkout develop
     git merge --no-ff release/1.0
     git branch -d release/1.0

  6. Hotfix (urgent production bug)
     git checkout -b hotfix/crash main
     git commit -m "Fix null pointer crash"
     git checkout main
     git merge --no-ff hotfix/crash
     git tag -a v1.0.1
     git checkout develop
     git merge --no-ff hotfix/crash
     git branch -d hotfix/crash

PROS: clear separation, good for scheduled releases
CONS: complex, many branches, slow for CI/CD
BEST FOR: large teams, versioned releases (mobile apps, enterprise)
```


## GitHub Flow (Simpler)

```
BRANCHES:
  main          — always deployable
  feature/*     — everything else

WORKFLOW:
  1. Create branch from main
     git checkout -b feature/login main

  2. Commit, push
     git push -u origin feature/login

  3. Open Pull Request on GitHub

  4. Code review, CI passes

  5. Merge to main (squash or merge commit)

  6. Deploy from main (auto or manual)

  7. Delete feature branch

PROS: simple, fast, CI/CD friendly
CONS: no staging/release branches
BEST FOR: web apps with continuous deployment, small-medium teams
```


## Trunk-Based Development

```
BRANCHES:
  main (trunk)  — everyone commits here
  short-lived   — <1 day feature branches (optional)

RULES:
  - Branches live at most 1-2 days
  - Merge to main multiple times per day
  - Feature flags for incomplete features
  - main is always releasable

WORKFLOW:
  1. Pull latest main
     git pull --rebase origin main

  2. Small change, commit directly or tiny branch
     git checkout -b feat/button
     git commit -m "Add submit button"
     git push && create PR → merge same day

  3. Feature flags for unfinished work
     if (featureFlags.newCheckout) { showNewCheckout(); }

PROS: fastest, least merge conflicts, encourages small changes
CONS: requires feature flags, needs strong CI, discipline
BEST FOR: mature teams, Google/Facebook style, continuous deployment
```


---

# CHAPTER 3: MERGE vs REBASE


## Merge

```bash
# Merge feature into main
git checkout main
git merge feature/login

# Three-way merge: finds common ancestor, combines changes
# Creates a MERGE COMMIT (2 parents)

# Fast-forward merge (linear history, no merge commit)
git merge --ff feature/login

# Always create merge commit (even if fast-forward possible)
git merge --no-ff feature/login

# Abort merge in progress
git merge --abort

MERGE COMMIT GRAPH:
  Before:
    main:    A──B──C
    feature:    └──D──E

  After merge:
    main:    A──B──C──────F  (F = merge commit, parents: C and E)
    feature:    └──D──E──┘
```


## Rebase

```bash
# Rebase feature onto main
git checkout feature/login
git rebase main

# Result: feature's commits REPLAYED on top of main
# Linear history, no merge commit

REBASE GRAPH:
  Before:
    main:    A──B──C
    feature:    └──D──E

  After rebase:
    main:    A──B──C
    feature:          └──D'──E'  (new commits, same changes)

  Then fast-forward merge:
    git checkout main
    git merge feature/login
    main:    A──B──C──D'──E'  (linear!)

# Interactive rebase (THE POWER TOOL)
git rebase -i HEAD~5           # Last 5 commits
git rebase -i main             # All commits since diverging from main

# Opens editor with:
pick a1b2c3d Add login form
pick 4e5f6a7 Fix typo
pick 8b9c0d1 Add validation
pick 2e3f4a5 Fix another typo
pick 6c7d8e9 Add tests

# Commands:
# pick   — keep commit as-is
# reword — keep commit, edit message
# edit   — pause at this commit (amend it)
# squash — meld into previous commit (keep both messages)
# fixup  — meld into previous, discard this message
# drop   — remove commit entirely
# reorder lines = reorder commits

# Common: squash fix commits into their parent
pick a1b2c3d Add login form
fixup 4e5f6a7 Fix typo
pick 8b9c0d1 Add validation
fixup 2e3f4a5 Fix another typo
pick 6c7d8e9 Add tests
# Result: 3 clean commits instead of 5

# Abort rebase
git rebase --abort

# Continue after resolving conflicts
git rebase --continue

# Skip current commit
git rebase --skip
```


## THE GOLDEN RULE

```
NEVER REBASE COMMITS THAT HAVE BEEN PUSHED TO A SHARED BRANCH.

Rebase rewrites history (new SHA hashes).
If others have the old commits → diverged history → chaos.

SAFE:
  ✅ Rebase your local feature branch onto main
  ✅ Interactive rebase your unpushed commits
  ✅ Rebase before pushing feature branch

DANGEROUS:
  ❌ Rebase main
  ❌ Rebase after pushing to shared branch
  ❌ git push --force to main

RECOVERY (if you did it):
  git push --force-with-lease origin feature
  # Safer than --force: fails if remote has new commits you haven't seen
```


## Merge vs Rebase: When to Use Which

```
USE MERGE WHEN:
  ✅ Merging feature into main (preserves context)
  ✅ You want to keep the full branch history
  ✅ Working with a team on same branch
  ✅ PR/MR workflow (GitHub/GitLab merge button)

USE REBASE WHEN:
  ✅ Updating your feature branch with latest main
  ✅ Cleaning up commits before PR (interactive rebase)
  ✅ You want linear history
  ✅ Solo work on a feature branch

COMMON WORKFLOW (best of both):
  1. Work on feature branch
  2. Before PR: rebase onto latest main (clean history)
     git checkout feature/login
     git fetch origin
     git rebase origin/main
  3. Push feature (force if needed for your branch only)
     git push --force-with-lease origin feature/login
  4. Create PR → merge (--no-ff or squash merge)
```


---

# CHAPTER 4: CONFLICT RESOLUTION


## Understanding Conflicts

```
CONFLICT HAPPENS WHEN:
  Two branches modified the SAME lines in the SAME file.
  Git can't decide which version to keep.

NOT A CONFLICT:
  Branch A edits file1.txt, Branch B edits file2.txt → auto-merged
  Branch A edits line 1, Branch B edits line 100 → auto-merged

IS A CONFLICT:
  Both branches edit line 42 differently → CONFLICT
```


## Resolving Merge Conflicts

```bash
# During merge, git shows:
Auto-merging src/auth.ts
CONFLICT (content): Merge conflict in src/auth.ts
Automatic merge failed; fix conflicts and then commit the result.

# In the file, Git inserts markers:
<<<<<<< HEAD
const timeout = 5000;
=======
const timeout = 10000;
>>>>>>> feature/login

# HEAD = your current branch (main)
# feature/login = the branch being merged

# TO RESOLVE:
# 1. Edit the file — pick one, combine, or rewrite
const timeout = 10000;   # Chose feature's version

# 2. Remove ALL conflict markers (<<<, ===, >>>)

# 3. Stage the resolved file
git add src/auth.ts

# 4. Continue
git commit                 # For merge
# or
git rebase --continue      # For rebase

# TOOLS:
git mergetool              # Opens configured merge tool
# Configure:
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait --merge $REMOTE $LOCAL $BASE $MERGED'

# VS Code: click "Accept Current", "Accept Incoming", "Accept Both"
```


## Preventing Conflicts

```
STRATEGIES:

1. PULL OFTEN
   git pull --rebase origin main
   Small, frequent syncs = small conflicts

2. SMALL, FOCUSED BRANCHES
   Big branch = weeks of divergence = nightmare merge
   Small branch = 1-2 days = easy merge

3. COMMUNICATE
   "I'm refactoring auth.ts" → others avoid editing it

4. MODULAR CODE
   Separate concerns into separate files
   Fewer people editing same file

5. FEATURE FLAGS
   Don't branch for weeks; merge daily behind a flag
```


---

# CHAPTER 5: UNDOING THINGS


## Amend Last Commit

```bash
# Fix last commit message
git commit --amend -m "Correct message"

# Add forgotten file to last commit
git add forgotten-file.txt
git commit --amend --no-edit     # Keep same message

# ONLY BEFORE PUSHING! After push, use revert instead.
```


## Reset — Move HEAD Backwards

```bash
# Soft: move HEAD, keep staging + working dir
git reset --soft HEAD~1
# Commit undone, changes still staged (ready to re-commit)

# Mixed (default): move HEAD, unstage, keep working dir
git reset HEAD~1
# Commit undone, changes in working dir (need to re-add)

# Hard: move HEAD, discard everything
git reset --hard HEAD~1
# ⚠️ DESTRUCTIVE! Changes GONE (unless reflog)

# Reset specific file (unstage)
git reset HEAD file.txt          # Unstage
git restore --staged file.txt    # Modern equivalent

# Reset to specific commit
git reset --hard abc123f

# GOLDEN RULE: Never reset commits that were pushed to shared branches
```


## Revert — Safe Undo

```bash
# Create a NEW commit that undoes a previous commit
git revert abc123f
# Safe for shared branches! History preserved.

# Revert merge commit (specify which parent to keep)
git revert -m 1 MERGE_COMMIT_HASH
# -m 1 = keep first parent (usually main)

# Revert without committing (stage only)
git revert --no-commit abc123f
```


## Restore — Discard Working Changes

```bash
# Discard unstaged changes in specific file
git restore file.txt

# Discard ALL unstaged changes
git restore .

# Restore from specific commit
git restore --source=HEAD~3 file.txt

# Unstage a file
git restore --staged file.txt
```


## Reflog — The Safety Net

```bash
# Reflog tracks EVERY HEAD movement (even resets, rebases)
git reflog
# Shows:
# a1b2c3d HEAD@{0}: commit: Add tests
# 4e5f6a7 HEAD@{1}: reset: moving to HEAD~1
# 8b9c0d1 HEAD@{2}: commit: Add validation (THIS was "lost"!)

# Recover "lost" commit
git checkout 8b9c0d1              # Detached HEAD at lost commit
git branch recovered-work         # Create branch to keep it
git checkout recovered-work

# Or reset back to it
git reset --hard 8b9c0d1

# Reflog entries expire after 90 days (default)
# So you have ~3 months to recover anything

# RULE: In Git, nothing is truly lost for 90 days.
# Even after --hard reset, reflog saves you.
```


## Cherry-Pick — Copy Specific Commits

```bash
# Copy a commit from another branch to current
git cherry-pick abc123f

# Multiple commits
git cherry-pick abc123f def456a

# Range (exclusive start)
git cherry-pick main..feature     # All commits in feature not in main

# Without committing (stage only)
git cherry-pick --no-commit abc123f

# USE CASES:
# - Hotfix: cherry-pick fix from develop into main
# - Backport: apply feature to older release branch
# - Accidentally committed to wrong branch

# CAUTION: creates NEW commit (different SHA)
# Can cause duplicate commits if later merged normally
```


---

# CHAPTER 6: ADVANCED OPERATIONS


## Bisect — Find Bug-Introducing Commit

```bash
# Binary search through commits to find when bug was introduced
git bisect start
git bisect bad                    # Current commit has the bug
git bisect good v1.0              # v1.0 was known good

# Git checks out middle commit. You test.
# If bug present:
git bisect bad
# If no bug:
git bisect good

# Repeat. Git narrows down to THE commit.
# After ~7 steps for 100 commits (log₂(100)).

# Finish
git bisect reset                  # Return to original branch

# AUTOMATED bisect (even better!)
git bisect start
git bisect bad HEAD
git bisect good v1.0
git bisect run npm test           # Runs test on each commit
# Git finds the EXACT commit that broke the test!

# Also works with custom scripts:
git bisect run ./check_bug.sh
# Script must exit 0 (good) or 1 (bad)
```


## Worktrees — Multiple Working Directories

```bash
# Work on 2 branches simultaneously WITHOUT stashing
git worktree add ../hotfix-dir hotfix/urgent
# Creates new directory at ../hotfix-dir with hotfix/urgent checked out

# Work in original dir: feature branch
# Work in ../hotfix-dir: hotfix branch
# No stashing, no switching, both open at once!

cd ../hotfix-dir
# Make fix, commit, push
git commit -m "Fix urgent bug"
git push

# Remove worktree when done
git worktree remove ../hotfix-dir

# List worktrees
git worktree list
```


## Submodules

```bash
# Add another repo inside yours
git submodule add https://github.com/org/lib.git libs/lib
git commit -m "Add lib submodule"

# Clone repo with submodules
git clone --recursive https://github.com/org/project.git
# Or after clone:
git submodule update --init --recursive

# Update submodule to latest
cd libs/lib
git pull origin main
cd ../..
git add libs/lib
git commit -m "Update lib to latest"

# PROBLEMS WITH SUBMODULES:
# - Detached HEAD inside submodule
# - Forget to push submodule before main repo
# - Colleagues forget --recursive

# ALTERNATIVES:
# - Git subtree (simpler, merges into main repo)
# - Package manager (npm, pip — better for libraries)
# - Monorepo tools (Nx, Turborepo, Lerna)
```


## Hooks

```bash
# Git hooks: scripts that run at specific events
# Located in .git/hooks/ (local only, not committed)

# Common hooks:
# pre-commit    — before commit (lint, format, test)
# commit-msg    — validate commit message
# pre-push      — before push (run tests)
# post-merge    — after merge (install deps)
# post-checkout — after checkout

# Example pre-commit hook:
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
set -e

echo "Running linter..."
npm run lint || { echo "Lint failed!"; exit 1; }

echo "Running tests..."
npm test || { echo "Tests failed!"; exit 1; }

echo "All checks passed!"
EOF
chmod +x .git/hooks/pre-commit

# BETTER: Use pre-commit framework (shareable hooks)
# pip install pre-commit

# .pre-commit-config.yaml (committed to repo!)
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: ['--maxkb=500']

  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
      - id: isort

# Install hooks
pre-commit install
# Now they run automatically on every commit
```


---

# CHAPTER 7: COLLABORATION PATTERNS


## Pull Request Best Practices

```
CREATING A GOOD PR:

TITLE:
  "Add user authentication with JWT"
  NOT "fix stuff" or "update files"

DESCRIPTION TEMPLATE:
  ## What
  Added JWT-based authentication for the API.
  
  ## Why
  Users need to log in to access protected resources.
  
  ## How
  - Added /auth/login and /auth/register endpoints
  - JWT tokens with 15min expiry + refresh tokens
  - Middleware for protected routes
  
  ## Testing
  - Unit tests for auth service
  - Integration test for login flow
  - Manual testing: login → access protected → refresh
  
  ## Screenshots (if UI)
  [screenshot of login page]

SIZE:
  ✅ < 400 lines changed (reviewable in 30 min)
  ⚠️ 400-1000 lines (needs focused review time)
  ❌ > 1000 lines (split into smaller PRs!)

  Smaller PRs = faster review = fewer bugs = happier team
```


## Code Review Guidelines

```
AS REVIEWER:

DO:
  ✅ Focus on logic, not style (linters handle style)
  ✅ Ask questions, don't demand ("What if X happens?")
  ✅ Acknowledge good code ("Nice approach!")
  ✅ Suggest alternatives, not just "wrong"
  ✅ Test locally if change is complex
  ✅ Review within 24 hours (don't block others)

DON'T:
  ❌ Nitpick formatting (automate with Prettier/Black)
  ❌ Rewrite their approach (suggest, don't dictate)
  ❌ Approve without reading (rubber-stamping)
  ❌ Block on opinions ("I would have done it differently")

COMMENT PREFIXES (convention):
  nit:      — minor, non-blocking (style preference)
  question: — clarification needed
  suggestion: — alternative approach to consider
  issue:    — must fix before merge
  praise:   — good work highlight

AS AUTHOR:
  ✅ Self-review before requesting others
  ✅ Respond to all comments (even just "Done")
  ✅ Don't take feedback personally
  ✅ Explain your reasoning if you disagree
```


## Commit Message Convention

```
CONVENTIONAL COMMITS (widely adopted):

FORMAT:
  <type>(<scope>): <description>

  [optional body]

  [optional footer(s)]

TYPES:
  feat:     New feature
  fix:      Bug fix
  docs:     Documentation only
  style:    Formatting (no logic change)
  refactor: Code change (no new feature, no bug fix)
  perf:     Performance improvement
  test:     Adding/fixing tests
  build:    Build system, dependencies
  ci:       CI/CD changes
  chore:    Maintenance tasks

EXAMPLES:
  feat(auth): add JWT authentication
  fix(api): handle null user in profile endpoint
  docs(readme): add setup instructions
  refactor(utils): extract date formatting to helper
  test(auth): add login integration tests
  perf(db): add index on users.email

BREAKING CHANGE:
  feat(api)!: rename /users endpoint to /accounts

  BREAKING CHANGE: The /users endpoint has been renamed to /accounts.
  Update all client code accordingly.

BODY (when needed):
  fix(parser): handle empty markdown files

  Previously the parser would crash with an IndexError when
  processing a markdown file with no content. Now it returns
  an empty list of chunks.

  Fixes #234

WHY THIS MATTERS:
  - Auto-generate CHANGELOG
  - Semantic versioning (feat = minor, fix = patch, ! = major)
  - Easy to search history
  - Tools: commitlint, semantic-release, release-please
```


## Git Aliases

```bash
# Add to ~/.gitconfig or run git config --global

[alias]
    # Short forms
    s = status
    co = checkout
    sw = switch
    br = branch
    ci = commit
    cp = cherry-pick

    # Log (pretty)
    lg = log --oneline --graph --all --decorate
    ll = log --pretty=format:'%C(yellow)%h%Creset %s %C(blue)(%ar)%Creset %C(red)%an%Creset' --abbrev-commit -20
    
    # Common workflows
    amend = commit --amend --no-edit
    undo = reset --soft HEAD~1
    unstage = restore --staged
    wip = commit -am "WIP"
    
    # Branch cleanup
    cleanup = "!git branch --merged | grep -v '\\*\\|main\\|develop' | xargs -n 1 git branch -d"
    
    # Diff tools
    df = diff --stat
    dfc = diff --cached --stat

    # Pull with rebase
    up = pull --rebase --autostash

    # Push current branch
    pushf = push --force-with-lease

# Usage:
git s             # git status
git lg            # Pretty log graph
git amend         # Amend without changing message
git undo          # Undo last commit (keep changes)
git up            # Pull + rebase + auto-stash
git cleanup       # Delete merged branches
```


---

# CHAPTER 8: ADVANCED GIT TECHNIQUES


## Blame — Find Who Changed What

```bash
# Show last modifier per line
git blame src/auth.ts

# Specific lines only
git blame -L 10,20 src/auth.ts

# Ignore whitespace changes
git blame -w src/auth.ts

# Show commit before the last change (find ORIGINAL author)
git blame --ignore-rev COMMIT_HASH src/auth.ts

# Bulk ignore (e.g., formatting commits)
echo FORMATTING_COMMIT_HASH > .git-blame-ignore-revs
git config blame.ignoreRevsFile .git-blame-ignore-revs
```


## Log — Search History

```bash
# Search commit messages
git log --grep="auth" --oneline

# Search code changes (find when function was added/removed)
git log -S "functionName" --oneline
# "Pickaxe" — finds commits that changed count of that string

# Search with regex
git log -G "TODO|FIXME" --oneline

# By author
git log --author="Alice" --oneline --since="2026-01-01"

# By file
git log -- src/auth.ts

# By date
git log --after="2026-06-01" --before="2026-06-10"

# Show stat (files changed per commit)
git log --stat --oneline -10

# Show diff in log
git log -p -1                         # Last commit with full diff

# Compact summary
git shortlog -sn                      # Commits per author
git shortlog -sn --since="2026-01-01" # This year
```


## Clean — Remove Untracked Files

```bash
# See what would be removed (dry run)
git clean -n

# Remove untracked files
git clean -f

# Remove untracked files AND directories
git clean -fd

# Remove ignored files too (e.g., build artifacts)
git clean -fdX             # Only ignored files
git clean -fdx             # Everything untracked + ignored

# Interactive
git clean -i
```


## Patch Files

```bash
# Create patch from last commit
git format-patch -1 HEAD
# Creates: 0001-commit-message.patch

# Create patch from multiple commits
git format-patch main..feature     # All commits in feature

# Apply patch
git am 0001-commit-message.patch
git am *.patch                      # Apply all

# Apply with 3-way merge (better conflict handling)
git am --3way 0001-*.patch

# Create diff patch (simpler, no commit info)
git diff > changes.patch
git apply changes.patch
```


## Large File Storage (Git LFS)

```bash
# Install
git lfs install

# Track file types
git lfs track "*.psd"
git lfs track "*.zip"
git lfs track "models/*.gguf"

# This creates/updates .gitattributes
cat .gitattributes
# *.psd filter=lfs diff=lfs merge=lfs -text

# Commit .gitattributes
git add .gitattributes
git commit -m "Track large files with LFS"

# Now add large files normally
git add model.gguf
git commit -m "Add model"
git push
# File stored in LFS server, repo has only pointer

# See what's in LFS
git lfs ls-files

# Pull LFS files (on clone)
git lfs pull
```


---

# CHAPTER 9: TROUBLESHOOTING


## Common Problems and Solutions

```bash
# PROBLEM: Committed to wrong branch
git stash                          # Save current work
git checkout correct-branch
git stash pop                      # Apply here

# Or: cherry-pick and reset
git checkout correct-branch
git cherry-pick abc123f            # Copy commit
git checkout wrong-branch
git reset --hard HEAD~1            # Remove from wrong branch


# PROBLEM: Accidentally deleted a branch
git reflog                         # Find the commit
git branch recovered abc123f       # Create branch at that commit


# PROBLEM: Want to split a commit into two
git rebase -i HEAD~3
# Change commit from 'pick' to 'edit'
git reset HEAD~1                   # Unstage commit's changes
git add file1.txt
git commit -m "First part"
git add file2.txt
git commit -m "Second part"
git rebase --continue


# PROBLEM: Merge conflict in binary file
git checkout --ours image.png      # Keep ours
git checkout --theirs image.png    # Keep theirs
git add image.png


# PROBLEM: Repo is huge (slow clone)
git clone --depth 1 URL            # Shallow clone (latest only)
git clone --filter=blob:none URL   # Blobless clone (fetch blobs on demand)


# PROBLEM: Need to change author of old commits
git rebase -i HEAD~5
# Mark commits as 'edit'
git commit --amend --author="New Name <email>" --no-edit
git rebase --continue


# PROBLEM: .gitignore not working (files already tracked)
git rm -r --cached .               # Untrack everything
git add .                          # Re-add with new .gitignore
git commit -m "Apply .gitignore"


# PROBLEM: Undo a push (DANGEROUS on shared branches!)
git push --force-with-lease origin branch
# Use --force-with-lease, NEVER plain --force

# PROBLEM: Find which commit deleted a file
git log --all --full-history -- path/to/file
# Recover it:
git checkout COMMIT_HASH^ -- path/to/file
```


## .gitignore Best Practices

```gitignore
# Dependencies
node_modules/
vendor/
venv/
.venv/
__pycache__/
*.pyc

# Build output
dist/
build/
*.o
*.class
target/

# IDE
.idea/
.vscode/settings.json    # Keep launch.json, share debug config
*.swp
*.swo
*~

# OS files
.DS_Store
Thumbs.db
desktop.ini

# Environment / secrets
.env
.env.*
!.env.example
*.pem
*.key
secrets/

# Logs
*.log
logs/

# Large files (if not using LFS)
*.zip
*.tar.gz
*.rar
*.gguf
*.bin

# Coverage
coverage/
.nyc_output/
htmlcov/

# Docker
docker-compose.override.yml
```


## Common Pitfalls

```
PITFALL 1: git push --force to main
  → Rewrites history for everyone. Use --force-with-lease on feature branches only.

PITFALL 2: Committing secrets (.env, API keys)
  → Use .gitignore. If committed: rotate the secret, use git filter-branch or BFG to remove.

PITFALL 3: Giant commits ("Update everything")
  → Small, focused commits with clear messages.

PITFALL 4: Never pulling before pushing
  → git pull --rebase before push. Prevents unnecessary merge commits.

PITFALL 5: Not using branches
  → Even solo, use branches for features. main stays clean.

PITFALL 6: Rebasing shared branches
  → Only rebase YOUR unpushed commits. Never rebase main or shared branches.

PITFALL 7: Ignoring merge conflicts
  → Resolve carefully. Run tests after. Don't just accept "theirs" blindly.

PITFALL 8: Binary files in Git
  → Use Git LFS for large binaries. Git is bad at binary diffs.

PITFALL 9: Messy history (WIP, fixup, oops commits)
  → Interactive rebase to clean up BEFORE pushing.

PITFALL 10: Not setting up .gitignore early
  → Add .gitignore FIRST COMMIT. node_modules in Git = pain forever.

PITFALL 11: Detached HEAD panic
  → Not dangerous! Just create a branch: git switch -c my-branch

PITFALL 12: Trusting git clean without -n
  → Always dry-run first: git clean -n, then git clean -f.
```