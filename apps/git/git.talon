tag: user.git
-

git:                            "git "
git verison:                    "git --version\n"
git init:                       "git init\n"
git status:                     "git status\n"
git log:                        "git log\n"
git reflog:                     "git reflog\n"
git clean:                      "git clean "
git remove:                     "git rm "
git tag [<user.text>]:          "git tag {text or ''}"
git merge [<user.text>]:        "git merge {text or ''}"
git branch [<user.text>]:       "git branch {text or ''}"
git remote:                     "git remote "
git clone:                      "git clone "
git cherry-pick:                "git cherry-pick "
git rebase:                     "git rebase "

git reset head:                 "git reset --soft HEAD^"
git reset [<user.text>]:        "git reset {text or ''}"
git reset soft [<user.text>]:   "git reset --soft {text or ''}"
git reset hard [<user.text>]:   "git reset --hard {text or ''}"

git fetch:                      "git fetch\n"
git fetch all:                  "git fetch -a\n"
git fetch [<user.text>]:        "git fetch {text or ''}"
git fetch upstream:             "git fetch upstream\n"

git checkout [<user.text>]:     "git checkout {text or ''}"
git checkout main:              "git checkout main\n"
git checkout master:            "git checkout master\n"
git checkout develop:           "git checkout develop\n"

git add [<user.text>]:          "git add {text or ''}"
git add dot:                    "git add .\n"

git commit:
    'git commit -m ""'
    key(left)
git commit <user.text>$:        'git commit -m "{text}"'
git commit amend:               "git commit --amend "

git diff:                       "git diff\n"
git diff <user.text>$:          "git diff {text}"

git pull:                       "git pull\n"
git pull upstream:              "git pull upstream\n"
git pull upstream master:       "git pull upstream master\n"

git push:                       "git push\n"
git push tags:                  "git push --tags\n"

git stash:                      "git stash "
git stash show:                 "git stash show\n"
git stash pop:                  "git stash pop"

git merge quit:
    ":q"
    key(enter)

git numstat:                    user.git_numstat("")
git numstat year:               user.git_numstat("1 year")
git numstat month:              user.git_numstat("1 month")
git numstat week:               user.git_numstat("1 week")