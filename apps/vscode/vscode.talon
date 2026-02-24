app: vscode
-
tag(): user.scroll
tag(): user.navigation
tag(): user.zoom
tag(): user.tabs
tag(): user.find
tag(): user.extensions
tag(): user.code_comments
tag(): user.git

settings():
    user.scroll_speed = 0.9

# Language features
jest:                       code.complete()
jest first:
    code.complete()
    key(tab)
jest param:                 user.run_rpc_command("editor.action.triggerParameterHints")
format document:            user.format_document()
refactor this:              user.run_rpc_command("editor.action.refactor")
open preview:               user.run_rpc_command("markdown.showPreview")
open preview split:         user.run_rpc_command("markdown.showPreviewToSide")

# Problems
problem next:               user.run_rpc_command("editor.action.marker.nextInFiles")
problem last:               user.run_rpc_command("editor.action.marker.prevInFiles")
problem fix:                user.run_rpc_command("problems.action.showQuickFixes")
(quick | kvick | pick) fix: user.run_rpc_command("editor.action.quickFix")

# Imports
imports organize:           user.run_rpc_command("editor.action.organizeImports")
imports add:                user.vscode_add_missing_imports()
imports fix:
    user.vscode_add_missing_imports()
    sleep(100ms)
    user.run_rpc_command("editor.action.organizeImports")

# Split
split up:                   user.run_rpc_command("workbench.action.moveEditorToAboveGroup")
split down:                 user.run_rpc_command("workbench.action.moveEditorToBelowGroup")
split left:                 user.run_rpc_command("workbench.action.moveEditorToLeftGroup")
split right:                user.run_rpc_command("workbench.action.moveEditorToRightGroup")
focus up:                   user.run_rpc_command("workbench.action.focusAboveGroup")
focus down:                 user.run_rpc_command("workbench.action.focusBelowGroup")
focus left:                 user.run_rpc_command("workbench.action.focusLeftGroup")
focus right:                user.run_rpc_command("workbench.action.focusRightGroup")
shrink width:               user.run_rpc_command("workbench.action.decreaseViewWidth")
shrink height:              user.run_rpc_command("workbench.action.decreaseViewHeight")
expand width:               user.run_rpc_command("workbench.action.increaseViewWidth")
expand height:              user.run_rpc_command("workbench.action.increaseViewHeight")
split flip:                 user.run_rpc_command("workbench.action.toggleEditorGroupLayout")
split clear:                user.run_rpc_command("workbench.action.joinTwoGroups")
split solo:                 user.run_rpc_command("workbench.action.editorLayoutSingle")
maximize:                   user.run_rpc_command("workbench.action.toggleEditorWidths")
cross:                      user.run_rpc_command("workbench.action.focusNextGroup")
open (cross | split):       key(alt-enter)

view grow:                  user.run_rpc_command("workbench.action.increaseViewSize")
view shrink:                user.run_rpc_command("workbench.action.decreaseViewSize")

# Sidebar
bar (show | hide):          user.run_rpc_command("workbench.action.toggleSidebarVisibility")
bar explore:                user.run_rpc_command("workbench.view.explorer")
bar extensions:             user.run_rpc_command("workbench.view.extensions")
bar outline:                user.run_rpc_command("outline.focus")
bar debug:                  user.run_rpc_command("workbench.view.debug")
bar search:                 user.run_rpc_command("workbench.view.search")
bar source:                 user.run_rpc_command("workbench.view.scm")
bar scopes:                 user.run_rpc_command("cursorless.scopes.focus")
bar active:                 user.run_rpc_command("workbench.files.action.showActiveFileInExplorer")
bar fold:                   user.run_rpc_command("workbench.files.action.collapseExplorerFolders")
ref last:                   user.run_rpc_command("references-view.prev")
ref next:                   user.run_rpc_command("references-view.next")

# Panel
panel (show | hide):        user.run_rpc_command("workbench.action.togglePanel")
panel (large | small):      user.run_rpc_command("workbench.action.toggleMaximizedPanel")
panel control:              user.run_rpc_command("workbench.panel.repl.view.focus")
panel output:               user.run_rpc_command("workbench.panel.output.focus")
panel problems:             user.run_rpc_command("workbench.panel.markers.view.focus")
panel terminal:             user.run_rpc_command("workbench.action.terminal.focus")
panel debug:                user.run_rpc_command("workbench.debug.action.toggleRepl")
panel clear:                user.run_rpc_command("workbench.debug.panel.action.clearReplAction")

# Chat
chat show:
    user.run_rpc_command("workbench.action.chat.open")
    user.run_rpc_command("workbench.action.restoreAuxiliaryBar")
codex show:
    user.run_rpc_command("chatgpt.sidebarView.focus")
    user.run_rpc_command("workbench.action.restoreAuxiliaryBar")
chat full:
    user.run_rpc_command("workbench.action.chat.open")
    user.run_rpc_command("workbench.action.maximizeAuxiliaryBar")
codex full:
    user.run_rpc_command("chatgpt.sidebarView.focus")
    user.run_rpc_command("workbench.action.maximizeAuxiliaryBar")
(chat | codex) hide:
    user.run_rpc_command("workbench.action.closeAuxiliaryBar")

# Hide sidebars, panel and widgets
hide all:
    user.run_rpc_command("workbench.action.closeSidebar")
    user.run_rpc_command("workbench.action.closeAuxiliaryBar")
    user.run_rpc_command("workbench.action.closePanel")
    user.run_rpc_command("closeFindWidget")

# Files / Folders
folder open:                user.run_rpc_command("workbench.action.files.openFolder")
folder add:                 user.run_rpc_command("workbench.action.addRootFolder")
folder new:                 user.run_rpc_command("explorer.newFolder")
file open:                  user.run_rpc_command("workbench.action.files.openFile")
file new [<user.filename>]:
    user.run_rpc_command("explorer.newFile")
    "{filename or ''}"
file open folder:           user.run_rpc_command("revealFileInOS")
file reveal:                user.run_rpc_command("workbench.files.action.showActiveFileInExplorer")
file revert:                user.run_rpc_command("workbench.action.files.revert")
file copy path:             user.run_rpc_command("copyFilePath")
file copy relative:         user.run_rpc_command("copyRelativeFilePath")
file copy name:             user.run_rpc_command("andreas.copyFilename")
file remove:                user.run_rpc_command("andreas.removeFile")
file move:                  user.run_rpc_command("andreas.moveFile")
file sibling [<user.filename>]:
    user.run_rpc_command("andreas.newFile", filename or "")
file rename [<user.filename>]:
    user.run_rpc_command("andreas.renameFile", filename or "")
file clone [<user.filename>]:
    user.run_rpc_command("andreas.duplicateFile", filename or "")

pop sibling:
    user.find_sibling_file()
    sleep(200ms)
    key(enter)

# Git
git open file:              user.git_open_remote_file_url(false, false)
git copy file:              user.git_copy_remote_file_url(false, false)
git open branch:            user.git_open_remote_file_url(false, true)
git copy branch:            user.git_copy_remote_file_url(false, true)
git (repo | repository):    user.git_open_url("Repo")
git issues:                 user.git_open_url("Issues")
git new issue:              user.git_open_url("NewIssue")
git pull requests:          user.git_open_url("PullRequests")
git diff files:             user.run_rpc_command("git.viewChanges")
git open:                   user.run_rpc_command("git.openFile")
git open pull:              user.run_rpc_command("pr.openPullRequestOnGitHub")

# Folding
# fold recursive:             user.run_rpc_command("editor.foldRecursively")
# unfold recursive:           user.run_rpc_command("editor.unfoldRecursively")
# fold all:                   user.run_rpc_command("editor.foldAll")
# unfold all:                 user.run_rpc_command("editor.unfoldAll")
# fold comments:              user.run_rpc_command("editor.foldAllBlockComments")

# Navigation
go line <number>:           edit.jump_line(number - 1)
pop back:                   user.run_rpc_command("workbench.action.openPreviousRecentlyUsedEditor")
pop forward:                user.run_rpc_command("workbench.action.openNextRecentlyUsedEditor")
focus editor:               user.run_rpc_command("workbench.action.focusActiveEditorGroup")

# Tabs
tab {user.letter} [{user.letter}]:
    user.run_rpc_command("andreas.focusTab", "{letter_1}{letter_2 or ''}")

# Cursor
cursor back:                user.run_rpc_command("cursorUndo")
cursor forward:             user.run_rpc_command("cursorRedo")
cursor up:                  user.run_rpc_command("editor.action.insertCursorAbove")
cursor down:                user.run_rpc_command("editor.action.insertCursorBelow")
cursor lines:               user.run_rpc_command("editor.action.insertCursorAtEndOfEachLineSelected")
cursor expand:              user.run_rpc_command("editor.action.smartSelect.expand")
cursor shrink:              user.run_rpc_command("editor.action.smartSelect.shrink")
cursor next:                user.run_rpc_command("editor.action.addSelectionToNextFindMatch")
cursor last:                user.run_rpc_command("editor.action.addSelectionToPreviousFindMatch")
cursor (breed | all):       user.run_rpc_command("editor.action.selectHighlights")
cursor skip:                user.run_rpc_command("editor.action.moveSelectionToNextFindMatch")

# Debug and run
build program:              user.run_rpc_command("workbench.action.tasks.build")
run program:                user.run_rpc_command("workbench.action.debug.run")
debug start:                user.run_rpc_command("workbench.action.debug.start")
breakpoint:                 user.run_rpc_command("editor.debug.action.toggleBreakpoint")
continue:                   user.run_rpc_command("workbench.action.debug.continue")
step over:                  user.run_rpc_command("workbench.action.debug.stepOver")
step into:                  user.run_rpc_command("workbench.action.debug.stepInto")
step out:                   user.run_rpc_command("workbench.action.debug.stepOut")
debug restart:              user.run_rpc_command("workbench.action.debug.restart")
debug pause:                user.run_rpc_command("workbench.action.debug.pause")
debug stop:                 user.run_rpc_command("workbench.action.debug.stop")
debug select [<user.prose>]:
    user.run_rpc_command("workbench.action.debug.selectandstart")
    insert(prose or "")
debug extension:
    user.run_rpc_command("workbench.action.debug.selectandstart")
    insert("run")
    key(enter)
debug test:
    user.run_rpc_command("workbench.action.debug.selectandstart")
    insert("test")
    key(enter)
debug test subset:
    user.run_rpc_command("workbench.action.debug.selectandstart")
    insert("test subset")
    key(enter)
run task compile:
    user.run_rpc_command("workbench.action.tasks.runTask")
    insert("compile")
    sleep(200ms)
    key(enter)
run task [<user.prose>]:
    user.run_rpc_command("workbench.action.tasks.runTask")
    insert(prose or "")
dev tools:                  user.run_rpc_command("workbench.action.toggleDevTools")
select element:             key(ctrl-shift-c)

# Find session
scout (sesh | recent) [<user.prose>]$:
    user.vscode_find_recent(prose or "")
pop sesh {user.vscode_sessions}$:
    user.vscode_find_recent(vscode_sessions)
    sleep(150ms)
    key(enter)
pop sesh [<user.prose>]$:
    user.vscode_find_recent(prose or "")
    sleep(150ms)
    key(enter)

# Find a symbol
scout symbol [<user.prose>]$:
    user.run_rpc_command("workbench.action.showAllSymbols")
    sleep(50ms)
    user.insert_formatted(prose or "", "CAMEL_CASE")

# Settings
open settings (json | jason):
    user.run_rpc_command("workbench.action.openSettingsJson")
open settings <user.prose>:
    app.preferences()
    sleep(200ms)
    insert(prose)

# CSV
align columns:              user.run_rpc_command("rainbow-csv.Align")
shrink columns:             user.run_rpc_command("rainbow-csv.Shrink")

# Misc
update extensions:          user.run_rpc_command("workbench.extensions.action.checkForUpdates")
install extension:          user.run_rpc_command("workbench.extensions.action.installVSIX")
window reload:              user.run_rpc_command("workbench.action.reloadWindow")
trim trailing:              user.run_rpc_command("editor.action.trimTrailingWhitespace")
inspect scope:              user.run_rpc_command("editor.action.inspectTMScopes")
disk raw:                   user.save_without_formatting()
disk files:                 user.run_rpc_command("workbench.action.files.saveFiles")
copy command id:            user.copy_command_id()
scout again:                user.run_rpc_command("rerunSearchEditorSearch")
generate range [from <number_small>]:
    user.run_rpc_command("andreas.generateRange", number_small or 1)

snip last:                  user.run_rpc_command("jumpToPrevSnippetPlaceholder")
[snip] next:                user.run_rpc_command("jumpToNextSnippetPlaceholder")

change language {user.code_language}:
    user.change_language(code_language)
    key(enter)

change language [<user.prose>]:
    user.change_language(prose or "")

please [<user.prose>]$:
    user.run_rpc_command("workbench.action.showCommands")
    insert(prose or "")
