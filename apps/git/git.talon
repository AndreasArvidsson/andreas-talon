tag: user.git
-

# git:                            "git "
git verison:                 "git --version\n"
git init:                    "git init\n"
git status:                  "git status\n"
git log:                     "git log\n"
git reflog:                  "git reflog\n"
git clean:                   "git clean "
git remove:                  "git rm "
git tag:                     "git tag "
git merge:                   "git merge "
git branch:                  "git branch "
git clone:                   "git clone "
git cherry pick:             "git cherry-pick "
git rebase:                  "git rebase "

git remote:                  "git remote "
git remote verbose:          "git remote -v\n"

git reset head:              "git reset --soft HEAD^"
git reset:                   "git reset "
git reset soft:              "git reset --soft "
git reset hard:              "git reset --hard "

git fetch:                   "git fetch "
git fetch all:               "git fetch -a\n"
git fetch upstream:          "git fetch upstream\n"
git fetch prune:             "git fetch --prune origin\n"

git checkout:                "git checkout "
git checkout <user.text>$:   "git checkout {text}"
git checkout branch:         "git checkout -b "
git checkout main:           "git checkout main\n"
git checkout master:         "git checkout master\n"
git checkout develop:        "git checkout develop\n"

git add:                     "git add "
git add all:                 "git add .\n"

git commit:
    'git commit -m ""'
    key(left)
git commit <user.text>$:
    'git commit -m "{text}"'
    key(left)
git commit amend:            "git commit --amend "

git diff:                    "git diff\n"
git diff <user.text>$:       "git diff {text}"

git pull:                    "git pull\n"
git pull upstream:           "git pull upstream\n"
git pull upstream master:    "git pull upstream master\n"

git push:                    "git push\n"
git push tags:               "git push --tags\n"

git stash:                   "git stash "
git stash show:              "git stash show\n"
git stash pop:               "git stash pop"

git merge quit:
    ":q"
    key(enter)

git numstat:                 user.git_numstat("")
git numstat year:            user.git_numstat("1 year")
git numstat month:           user.git_numstat("1 month")
git numstat week:            user.git_numstat("1 week")