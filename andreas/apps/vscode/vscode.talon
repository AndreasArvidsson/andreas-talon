app: vscode
-
tag(): user.ide

settings():
    key_wait = 1

# Language features
suggest param:           user.vscode("editor.action.triggerParameterHints")
imports organize:        user.vscode("editor.action.organizeImports")
problem next:            user.vscode("editor.action.marker.nextInFiles")
problem last:            user.vscode("editor.action.marker.prevInFiles")
problem fix:             user.vscode("problems.action.showQuickFixes")
rename this:             user.vscode("editor.action.rename")
refactor this:           user.vscode("editor.action.refactor")
whitespace trim:         user.vscode("editor.action.trimTrailingWhitespace")

# Split
split up:                user.vscode("workbench.action.moveEditorToAboveGroup")
split down:              user.vscode("workbench.action.moveEditorToBelowGroup")
split left:              user.vscode("workbench.action.moveEditorToLeftGroup")
split right:             user.vscode("workbench.action.moveEditorToRightGroup")
focus up:                user.vscode("workbench.action.focusAboveGroup")
focus down:              user.vscode("workbench.action.focusBelowGroup")
focus left:              user.vscode("workbench.action.focusLeftGroup")
focus right:             user.vscode("workbench.action.focusRightGroup")
split flip:              user.vscode("workbench.action.toggleEditorGroupLayout")
split clear:             user.vscode("workbench.action.joinTwoGroups")
split clear all:         user.vscode("workbench.action.editorLayoutSingle")

# Sidebar
bar explorer:            user.vscode("workbench.view.explorer")
bar extensions:          user.vscode("workbench.view.extensions")
bar outline:             user.vscode("outline.focus")
bar run:                 user.vscode("workbench.view.debug")
bar search:              user.vscode("workbench.view.search")
bar source:              user.vscode("workbench.view.scm")
bar (show | hide):       user.vscode("workbench.action.toggleSidebarVisibility")
bar file:                user.vscode("workbench.files.action.showActiveFileInExplorer")
bar results:             key(ctrl-down)

# Panels
panel (show | hide):     user.vscode("workbench.action.togglePanel")
panel control:           user.vscode("workbench.panel.repl.view.focus")
panel output:            user.vscode("workbench.panel.output.focus")
panel problems:          user.vscode("workbench.panel.markers.view.focus")
panel terminal:          user.vscode("workbench.action.terminal.focus")
panel debug:             user.vscode("workbench.debug.action.toggleRepl")
focus editor:            user.vscode("workbench.action.focusActiveEditorGroup")

# Files / Folders
folder add:              user.vscode("workbench.action.addRootFolder")
folder new:              user.vscode("explorer.newFolder")
file open:               user.vscode("workbench.action.files.openFile")
file new:                user.vscode("explorer.newFile")
file open folder:        user.vscode("revealFileInOS")
file copy path:          user.vscode("copyFilePath")

# Folding
fold that:               user.vscode("editor.fold")
unfold that:             user.vscode("editor.unfold")
fold recursive:          user.vscode("editor.foldAllMarkerRegions")
unfold recursive:        user.vscode("editor.unfoldRecursively")
fold all:                user.vscode("editor.foldAll")
unfold all:              user.vscode("editor.unfoldAll")
fold comments:           user.vscode("editor.foldAllBlockComments")

# Navigation
go back:                 user.vscode("workbench.action.navigateBack")
go forward:              user.vscode("workbench.action.navigateForward")
take next:               user.vscode("editor.action.addSelectionToNextFindMatch")
take all these:          user.vscode("editor.action.selectHighlights")

# Scroll
large up:                key(alt-pageup)
large down:              key(alt-pagedown)
small up:                key(ctrl-up)
small down:              key(ctrl-down)

# Misc
install extension:       user.vscode("workbench.extensions.action.installVSIX")
minimap (show | hide):   user.vscode("editor.action.toggleMinimap")
show settings:           user.vscode("workbench.action.openGlobalSettings")
dev tools:               user.vscode("workbench.action.toggleDevTools")

please [<user.text>]:
    user.vscode("workbench.action.showCommands")
    insert(user.text or "")