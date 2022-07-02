tag: user.git
-

git verison:                "git --version\n"
git init:                   "git init\n"
git status:                 "git status\n"
git log:                    "git log --graph --color=always --format='%C(auto)%h%d %s %C(green)(%cr) %C(bold blue)<%an>%Creset'\n"
git log original:           "git log\n"
git reflog:                 "git reflog\n"
git clean:                  "git clean "
git remove:                 "git rm "
git tag:                    "git tag "
git branch:                 "git branch "
git branch deli:            "git branch -d "
git clone:                  "git clone "
git cherry pick:            "git cherry-pick "
git rebase:                 "git rebase "

git merge:                  "git merge "
git merge {user.git_branch}:
    "git merge {git_branch}"

git remote:                 "git remote "
git remote verbose:         "git remote -v\n"

git reset:                  "git reset "
git reset all:              "git reset .\n"
git reset head:             "git reset --soft HEAD^"
git reset soft:             "git reset --soft "
git reset hard:             "git reset --hard "

git fetch:                  "git fetch "
git fetch all:              "git fetch -a\n"
git fetch upstream:         "git fetch upstream\n"
git fetch prune:            "git fetch --prune origin\n"

git checkout:               "git checkout "
git checkout {user.git_branch}:
    "git checkout {git_branch}\n"
git checkout <user.text>:   "git checkout {text}"
git checkout branch:        "git checkout -b "
git checkout branch <user.text>:
    "git checkout -b {text}"
git checkout last:          "git checkout -\n"

git add:                    "git add "
git add all:                "git add .\n"

git commit:
    'git commit -m ""'
    key(left)
git commit <user.text>$:
    text = user.format_text(text, "CAPITALIZE_FIRST_WORD")
    'git commit -m "{text}"'
    key(left)
git commit amend:           "git commit --amend "

git diff:                   "git diff\n"
git diff halt:              "git diff "
git diff <user.text>:       "git diff {text}"

git pull:                   "git pull\n"
git pull upstream:          "git pull upstream\n"
git pull upstream master:   "git pull upstream master\n"
git pull upstream main:     "git pull upstream main\n"

git push:                   "git push\n"
git push tags:              "git push --tags\n"

git stash:                  "git stash "
git stash show:             "git stash show\n"
git stash pop:              "git stash pop"

git merge quit:
    ":q"
    key(enter)

git numstat:                user.git_numstat("")
git numstat year:           user.git_numstat("1 year")
git numstat month:          user.git_numstat("1 month")
git numstat week:           user.git_numstat("1 week")