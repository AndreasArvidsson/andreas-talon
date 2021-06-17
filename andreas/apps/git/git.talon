tag: user.git
-

git verison:                "git --version\n"
git init:                   "git init\n"
git status:                 "git status\n"
git log:                    "git log\n"
git fetch:                  "git fetch\n"
git clean:                  "git clean "
git remove:                 "git rm "
git tag  [<user.text>]:     "git tag {text or ''}"
git merge [<user.text>]:    "git merge {text or ''}"
git reset [<user.text>]:    "git reset {text or ''}"
git branch [<user.text>]:   "git branch {text or ''}"
git clone [<user.text>]:    "git clone {text or ''}"

git checkout:               "git checkout "
git checkout main:          "git checkout main\n"
git checkout master:        "git checkout master\n"
git checkout develop:       "git checkout develop\n"
git checkout <user.text>:   "git checkout {text}"

git add [<user.text>]:      "git add {text or ''}"
git add all:                "git add .\n"

git commit:
	'git commit -m ""'
	key(left)
git commit <user.text>:     'git commit -m "{text}"'

git diff:                   "git diff\n"
git diff <user.text>:       "git diff {text}"

git pull:                   "git pull\n"
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