app: vscode
-
tag(): user.scroll
tag(): user.navigation
tag(): user.zoom
tag(): user.tabs
tag(): user.find
tag(): user.comments

settings():
    user.scroll_speed = 0.9

# Language features
jest:                       code.complete()
jest first:
    code.complete()
    key(tab)
jest param:                 user.vscode("editor.action.triggerParameterHints")
format document:            user.format_document()
refactor this:              user.vscode("editor.action.refactor")
open preview:               user.vscode("markdown.showPreviewToSide")

# Problems
problem next:               user.vscode("editor.action.marker.nextInFiles")
problem last:               user.vscode("editor.action.marker.prevInFiles")
problem fix:                user.vscode("problems.action.showQuickFixes")
quick fix:                  user.vscode("editor.action.quickFix")

# Imports
imports organize:           user.vscode("editor.action.organizeImports")
imports add:                user.vscode_add_missing_imports()
imports fix:
    user.vscode_add_missing_imports()
    sleep(100ms)
    user.vscode("editor.action.organizeImports")

# Split
split up:                   user.vscode("workbench.action.moveEditorToAboveGroup")
split down:                 user.vscode("workbench.action.moveEditorToBelowGroup")
split left:                 user.vscode("workbench.action.moveEditorToLeftGroup")
split right:                user.vscode("workbench.action.moveEditorToRightGroup")
focus up:                   user.vscode("workbench.action.focusAboveGroup")
focus down:                 user.vscode("workbench.action.focusBelowGroup")
focus left:                 user.vscode("workbench.action.focusLeftGroup")
focus right:                user.vscode("workbench.action.focusRightGroup")
shrink width:               user.vscode("workbench.action.decreaseViewWidth")
shrink height:              user.vscode("workbench.action.decreaseViewHeight")
expand width:               user.vscode("workbench.action.increaseViewWidth")
expand height:              user.vscode("workbench.action.increaseViewHeight")
split flip:                 user.vscode("workbench.action.toggleEditorGroupLayout")
split clear:                user.vscode("workbench.action.joinTwoGroups")
split solo:                 user.vscode("workbench.action.editorLayoutSingle")
maximize:                   user.vscode("workbench.action.toggleEditorWidths")
cross:                      user.vscode("workbench.action.focusNextGroup")
open (cross | split):       key(alt-enter)

# Sidebar
bar (show | hide):          user.vscode("workbench.action.toggleSidebarVisibility")
bar explore:                user.vscode("workbench.view.explorer")
bar extensions:             user.vscode("workbench.view.extensions")
bar outline:                user.vscode("outline.focus")
bar debug:                  user.vscode("workbench.view.debug")
bar search:                 user.vscode("workbench.view.search")
bar source:                 user.vscode("workbench.view.scm")
bar file:                   user.vscode("workbench.files.action.showActiveFileInExplorer")
bar collapse:               user.vscode("workbench.files.action.collapseExplorerFolders")
ref last:                   user.vscode("references-view.prev")
ref next:                   user.vscode("references-view.next")

# Panel
panel (show | hide):        user.vscode("workbench.action.togglePanel")
panel (large | small):      user.vscode("workbench.action.toggleMaximizedPanel")
panel control:              user.vscode("workbench.panel.repl.view.focus")
panel output:               user.vscode("workbench.panel.output.focus")
panel problems:             user.vscode("workbench.panel.markers.view.focus")
panel terminal:             user.vscode("workbench.action.terminal.focus")
panel debug:                user.vscode("workbench.debug.action.toggleRepl")
panel clear:                user.vscode("workbench.debug.panel.action.clearReplAction")

# Hide sidebar and panel
hide all:
    user.vscode("workbench.action.closeSidebar")
    user.vscode("workbench.action.closePanel")
    user.vscode("closeFindWidget")

# Files / Folders
folder open:                user.vscode("workbench.action.files.openFolder")
folder add:                 user.vscode("workbench.action.addRootFolder")
folder new:                 user.vscode("explorer.newFolder")
file open:                  user.vscode("workbench.action.files.openFile")
file new [<user.filename>]:
    user.vscode("explorer.newFile")
    "{filename or ''}"
file open folder:           user.vscode("revealFileInOS")
file reveal:                user.vscode("workbench.files.action.showActiveFileInExplorer")
file revert:                user.vscode("workbench.action.files.revert")
file copy path:             user.vscode("copyFilePath")
file copy relative:         user.vscode("copyRelativeFilePath")
file copy name:             user.vscode("andreas.copyFilename")
file remove:                user.vscode("andreas.removeFile")
file move:                  user.vscode("andreas.moveFile")
file sibling [<user.filename>]:
    user.vscode("andreas.newFile", filename or "")
file rename [<user.filename>]:
    user.vscode("andreas.renameFile", filename or "")
file clone [<user.filename>]:
    user.vscode("andreas.duplicateFile", filename or "")

pop sibling:
    user.find_sibling_file()
    sleep(150ms)
    key(enter)

# Git
git open file:              user.git_open_remote_file_url(false, false)
git copy file:              user.git_copy_remote_file_url(false, false)
git open branch:            user.git_open_remote_file_url(false, true)
git copy branch:            user.git_copy_remote_file_url(false, true)
git repo:                   user.git_open_url("Repo")
git issues:                 user.git_open_url("Issues")
git new issue:              user.git_open_url("NewIssue")
git pull requests:          user.git_open_url("PullRequests")
git status:                 user.vscode("workbench.scm.focus")
git (changes | diff):       user.vscode("git.openChange")
git changed files:          user.vscode("git.openAllChanges")
git add all:                user.vscode("git.stageAll")
git reset all:              user.vscode("git.unstageAll")
git pull:                   user.vscode("git.pull")
git push:                   user.vscode("git.push")
git create tag:             user.vscode("git.createTag")
git push tags:              user.vscode("git.pushTags")
git open:                   user.vscode("git.openFile")
git stash:                  user.vscode("git.stash")
git stash pop:              user.vscode("git.stashPop")
git branch deli:            user.vscode("git.deleteBranch")
git merge:                  user.vscode("git.merge")
git merge {user.git_branch}:
    user.vscode("git.merge")
    sleep(50ms)
    "{git_branch}"
git checkout {user.git_branch}: user.git_find_branch(git_branch)
git checkout [<user.text>]: user.git_find_branch(text or "")
git checkout branch [<user.text>]:
    user.vscode("git.branch")
    sleep(50ms)
    text = user.format_text(text or '', "SNAKE_CASE")
    "{text}"
git commit [<user.text>]:
    user.vscode("git.commit")
    sleep(300ms)
    text = user.format_text(text or "", "SENTENCE")
    "{text}"

# Folding
fold recursive:             user.vscode("editor.foldRecursively")
unfold recursive:           user.vscode("editor.unfoldRecursively")
fold all:                   user.vscode("editor.foldAll")
unfold all:                 user.vscode("editor.unfoldAll")
fold comments:              user.vscode("editor.foldAllBlockComments")

# Navigation
go line <number>:           edit.jump_line(number)
pop back:                   user.vscode("workbench.action.openPreviousRecentlyUsedEditor")
pop forward:                user.vscode("workbench.action.openNextRecentlyUsedEditor")
focus editor:               user.vscode("workbench.action.focusActiveEditorGroup")

# Tabs
tab {self.letter} [{self.letter}]:
    user.vscode("andreas.focusTab", "{letter_1}{letter_2 or ''}")

# Cursor
cursor back:                user.vscode("cursorUndo")
cursor forward:             user.vscode("cursorRedo")
cursor up:                  user.vscode("editor.action.insertCursorAbove")
cursor down:                user.vscode("editor.action.insertCursorBelow")
cursor lines:               user.vscode("editor.action.insertCursorAtEndOfEachLineSelected")
cursor expand:              user.vscode("editor.action.smartSelect.expand")
cursor shrink:              user.vscode("editor.action.smartSelect.shrink")
cursor next:                user.vscode("editor.action.addSelectionToNextFindMatch")
cursor last:                user.vscode("editor.action.addSelectionToPreviousFindMatch")
cursor (breed | all):       user.vscode("editor.action.selectHighlights")
cursor skip:                user.vscode("editor.action.moveSelectionToNextFindMatch")

# Debug and run
build program:              user.vscode("workbench.action.tasks.build")
run program:                user.vscode("workbench.action.debug.run")
debug start:                user.vscode("workbench.action.debug.start")
breakpoint:                 user.vscode("editor.debug.action.toggleBreakpoint")
continue:                   user.vscode("workbench.action.debug.continue")
step over:                  user.vscode("workbench.action.debug.stepOver")
step into:                  user.vscode("workbench.action.debug.stepInto")
step out:                   user.vscode("workbench.action.debug.stepOut")
debug restart:              user.vscode("workbench.action.debug.restart")
debug pause:                user.vscode("workbench.action.debug.pause")
debug stop:                 user.vscode("workbench.action.debug.stop")
debug select:               user.vscode("workbench.action.debug.selectandstart")
debug extension:
    user.vscode("workbench.action.debug.selectandstart")
    "run extension"
    key(enter)
debug test:
    user.vscode("workbench.action.debug.selectandstart")
    "extension tests"
    key(enter)
debug subset:
    user.vscode("workbench.action.debug.selectandstart")
    "run test subset"
    key(enter)
run task compile:
    user.vscode("workbench.action.tasks.runTask")
    "compile"
    sleep(200ms)
    key(enter)
run task [<user.text>]:
    user.vscode("workbench.action.tasks.runTask")
    "{text or ''}"
dev tools:                  user.vscode("workbench.action.toggleDevTools")
select element:             key(ctrl-shift-c)

# Find session
scout (sesh | recent) [<user.text>]$:
    user.vscode_find_recent(text or "")
pop sesh {user.vscode_sessions}$:
    user.vscode_find_recent(vscode_sessions)
    sleep(150ms)
    key(enter)
pop sesh [<user.text>]$:
    user.vscode_find_recent(text or "")
    sleep(150ms)
    key(enter)

# Find a symbol
scout symbol [<user.text>]$:
    user.vscode("workbench.action.showAllSymbols")
    sleep(50ms)
    user.insert_formatted(text or "", "CAMEL_CASE")

# Settings
open settings json:
    user.vscode("workbench.action.openSettingsJson")
open settings <user.text>:
    app.preferences()
    sleep(200ms)
    "{text}"

# CSV
align columns:              user.vscode("rainbow-csv.Align")
shrink columns:             user.vscode("rainbow-csv.Shrink")

# Misc
install extension:          user.vscode("workbench.extensions.action.installVSIX")
window reload:              user.vscode("workbench.action.reloadWindow")
trim trailing:              user.vscode("editor.action.trimTrailingWhitespace")
inspect scope:              user.vscode("editor.action.inspectTMScopes")
disk raw:                   user.save_without_formatting()
disk files:                 user.vscode("workbench.action.files.saveFiles")
copy command id:            user.copy_command_id()
scout again:                user.vscode("rerunSearchEditorSearch")
generate range [from <number_small>]:
    user.vscode("andreas.generateRange", number_small or 1)

snip last:                  user.vscode("jumpToPrevSnippetPlaceholder")
[snip] next:                user.vscode("jumpToNextSnippetPlaceholder")

change language {user.code_language}:
    user.change_language(code_language)
    key(enter)

change language [<user.text>]:
    user.change_language(text or "")

please [<user.text>]$:
    user.vscode("workbench.action.showCommands")
    "{user.text or ''}"
