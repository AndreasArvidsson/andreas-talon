app: vscode
-
tag(): user.scroll
tag(): user.navigation
tag(): user.zoom
tag(): user.tabs
tag(): user.find
tag(): user.comments
tag(): user.cursorless_experimental_snippets

settings():
    user.scroll_step = 0.025

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
open cross:                 key(ctrl-enter)

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

# Experimental locate api
<user.vscode_panel> grab line:
    user.vscode_grab_line(vscode_panel)
<user.vscode_panel> snap {user.resize_size}:
    user.vscode_resize_panel(vscode_panel, resize_size)

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
file new:                   user.vscode("explorer.newFile")
file open folder:           user.vscode("revealFileInOS")
file reveal:                user.vscode("workbench.files.action.showActiveFileInExplorer")
file copy path:
    user.vscode("copyFilePath")
    user.clipboard_manager_update()
file copy relative:
    user.vscode("copyRelativeFilePath")
    user.clipboard_manager_update()
file copy name:
    name = user.vscode_get("andreas.getFileName")
    clip.set_text(name)
file clone:                 user.vscode("fileutils.duplicateFile")
file rename:                user.vscode("fileutils.renameFile")
file remove:                user.vscode("fileutils.removeFile")
file move:                  user.vscode("fileutils.moveFile")
pop sibling:
    user.find_sibling_file()
    sleep(150ms)
    key(enter)

# Git
git open file:              user.git_open_remote_file_url()
git copy file:              user.git_copy_remote_file_url()
git changes:                user.vscode("git.openChange")
git changed files:          user.vscode("git.openAllChanges")
git add all:                user.vscode("git.stageAll")
git reset all:              user.vscode("git.unstageAll")
git pull:                   user.vscode("git.pull")
git push:                   user.vscode("git.push")
git push tags:              user.vscode("git.pushTags")
git checkout {user.git_branch}: user.git_find_branch(git_branch)
git checkout [<user.text>]: user.git_find_branch(text or "")
git commit [<user.text>]:
    user.vscode("git.commit")
    text = user.format_text(text or "", "CAPITALIZE_FIRST_WORD")
    "{text}"

# Folding
fold this:                  user.vscode("editor.fold")
unfold this:                user.vscode("editor.unfold")
fold recursive:             user.vscode("editor.foldRecursively")
unfold recursive:           user.vscode("editor.unfoldRecursively")
fold all:                   user.vscode("editor.foldAll")
unfold all:                 user.vscode("editor.unfoldAll")
fold comments:              user.vscode("editor.foldAllBlockComments")

# Navigation
go line <number>:           edit.jump_line(number)
take word back:             user.vscode("editor.action.addSelectionToPreviousFindMatch")
cursor back:                user.vscode("cursorUndo")
cursor forward:             user.vscode("cursorRedo")
cursor up:                  user.vscode("editor.action.insertCursorAbove")
cursor down:                user.vscode("editor.action.insertCursorBelow")
cursor lines:               user.vscode("editor.action.insertCursorAtEndOfEachLineSelected")
cursor expand:              user.vscode("editor.action.smartSelect.expand")
cursor shrink:              user.vscode("editor.action.smartSelect.shrink")
pop back:                   user.vscode("workbench.action.openPreviousRecentlyUsedEditor")
pop forward:                user.vscode("workbench.action.openNextRecentlyUsedEditor")
focus editor:               user.vscode("workbench.action.focusActiveEditorGroup")

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
pop (sesh | recent) <user.text>$:
    user.vscode_find_recent(text)
    key(enter)
pop (sesh | recent):
    user.vscode_find_recent("", 1)
    key(enter)

# Find a symbol
scout symbol [<user.text>]$:
    user.vscode("workbench.action.gotoSymbol")
    "{text}"
scout all symbol [<user.text>]$:
    user.vscode("workbench.action.showAllSymbols")
    "{text}"

# Find miscellaneous
scout again:                user.vscode("rerunSearchEditorSearch")

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

# Cursorless
^cursorless use release$:
    user.cursorless_use_release()
^cursorless use develop$:
    user.cursorless_use_develop()
^cursorless record$:
    user.vscode("cursorless.recordTestCase")
^cursorless record highlight$:
    argument = user.to_dict("isDecorationsTest", 1)
    user.vscode("cursorless.recordTestCase", argument)
^cursorless record error$:
    argument = user.to_dict("recordErrors", 1)
    user.vscode("cursorless.recordTestCase", argument)
^cursorless record pause$:
    user.vscode("cursorless.pauseRecording")
^cursorless record resume$:
    user.vscode("cursorless.resumeRecording")

copy <user.cursorless_target>:
    user.cursorless_command("copyToClipboard", cursorless_target)
    user.clipboard_manager_update()
cut <user.cursorless_target>:
    user.cursorless_command("cutToClipboard", cursorless_target)
    user.clipboard_manager_update()
break line <user.cursorless_target>:
    user.cursorless_command("setSelectionBefore", cursorless_target)
    key("enter")
git open <user.cursorless_target>:
    user.cursorless_command("setSelection", cursorless_target)
    user.git_open_remote_file_url(1)
git copy <user.cursorless_target>:
    user.cursorless_command("setSelection", cursorless_target)
    user.git_copy_remote_file_url(1)
git copy mark [down] <user.cursorless_target>:
    user.cursorless_command("setSelection", cursorless_target)
    user.git_copy_markdown_remote_file_url(0)
git copy mark [down] <user.cursorless_primitive_target> [as <user.cursorless_primitive_target>]:
    user.git_copy_markdown_remote_file_url(cursorless_primitive_target_list)
paste <number_small> [and <number_small>]* <user.cursorless_positional_target>:
    user.clipboard_manager_copy(number_small_list)
    user.cursorless_command("pasteFromClipboard", cursorless_positional_target)

# Misc
install extension:          user.vscode("workbench.extensions.action.installVSIX")
window reload:              user.vscode("workbench.action.reloadWindow")
trim trailing:              user.vscode("editor.action.trimTrailingWhitespace")
inspect scope:              user.vscode("editor.action.inspectTMScopes")
disk raw:                   user.save_without_formatting()
disk files:                 user.vscode("workbench.action.files.saveFiles")
undo everything:            user.vscode("andreas.undoUntilNotDirty")
copy command id:            user.copy_command_id()

snip last:                  user.vscode("jumpToPrevSnippetPlaceholder")
[snip] next:                user.vscode("jumpToNextSnippetPlaceholder")

change language [<user.text>]:
    user.change_language(text or "")

please [<user.text>]$:
    user.vscode("workbench.action.showCommands")
    "{user.text or ''}"
