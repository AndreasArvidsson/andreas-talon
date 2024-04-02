tag: user.git
-

git clone:                  user.git_clone()

git status:                 user.git_status()

git add all:                user.git_stage_all()
git reset all:              user.git_unstage_all()

git pull:                   user.git_pull()
git push:                   user.git_push()
git push tags:              user.git_push_tags()

git tag:                    user.git_create_tag()
git tag list:               user.git_show_tags()

git stash:                  user.git_stash()
git stash pop:              user.git_stash_pop()

git merge [<user.text>]:    user.git_merge(text or "")
git merge {user.git_branch}:
    user.git_merge(git_branch)

git checkout [<user.text>]:
    text = user.format_text(text or "", "SNAKE_CASE")
    user.git_checkout(text)
git checkout {user.git_branch}:
    user.git_checkout(git_branch, true)

git checkout branch [<user.text>]:
    text = user.format_text(text or "", "SNAKE_CASE")
    user.git_create_branch(text)

git branch deli [<user.text>]:
    text = user.format_text(text or "", "SNAKE_CASE")
    user.git_delete_branch(text)

git branch:                 user.git_show_branches()

git commit [<user.text>]$:
    text = user.format_text(text or "", "SENTENCE")
    user.git_commit(text)
git commit amend [<user.text>]$:
    text = user.format_text(text or "", "SENTENCE")
    user.git_commit_amend(text)
git commit empty:
    user.git_commit_empty()

git diff:                   user.git_diff()

git stash show:             user.git_stash_show()
git stash list:             user.git_stash_list()

git log:                    user.git_log()
git remote:                 user.git_remote()

git cherry pick:            user.git_cherry_pick()
