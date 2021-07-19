app: vscode
-
tag(): user.ide
tag(): user.scroll

# Language features
suggest param:           user.vscode("editor.action.triggerParameterHints")
imports organize:        user.vscode("editor.action.organizeImports")
problem next:            user.vscode("editor.action.marker.nextInFiles")
problem last:            user.vscode("editor.action.marker.prevInFiles")
problem fix:             user.vscode("problems.action.showQuickFixes")
rename (this | dis):     user.vscode("editor.action.rename")
refactor (this | dis):   user.vscode("editor.action.refactor")
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
cross:                   user.vscode("workbench.action.focusNextGroup")

# Sidebar
bar (show | hide):       user.vscode("workbench.action.toggleSidebarVisibility")
bar explorer:            user.vscode("workbench.view.explorer")
bar extensions:          user.vscode("workbench.view.extensions")
bar outline:             user.vscode("outline.focus")
bar run:                 user.vscode("workbench.view.debug")
bar search:              user.vscode("workbench.view.search")
bar source:              user.vscode("workbench.view.scm")
bar file:                user.vscode("workbench.files.action.showActiveFileInExplorer")
bar results:             user.vscode("search.action.focusSearchList")

# Panel
panel (show | hide):     user.vscode("workbench.action.togglePanel")
panel (large | small):   user.vscode("workbench.action.toggleMaximizedPanel")
panel control:           user.vscode("workbench.panel.repl.view.focus")
panel output:            user.vscode("workbench.panel.output.focus")
panel problems:          user.vscode("workbench.panel.markers.view.focus")
panel terminal:          user.vscode("workbench.action.terminal.focus")
panel debug:             user.vscode("workbench.debug.action.toggleRepl")
panel clear:             user.vscode("workbench.debug.panel.action.clearReplAction")

# Focus editor
focus editor:            user.vscode("workbench.action.focusActiveEditorGroup")

# Hide sidebar and panel
hide all:
    user.vscode("workbench.action.closeSidebar")
    user.vscode("workbench.action.closePanel")

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
take last:               user.vscode("editor.action.addSelectionToPreviousFindMatch")
take all these:          user.vscode("editor.action.selectHighlights")

# Misc
install extension:       user.vscode("workbench.extensions.action.installVSIX")
minimap (show | hide):   user.vscode("editor.action.toggleMinimap")
dev tools:               user.vscode("workbench.action.toggleDevTools")
reload window:           user.vscode("workbench.action.reloadWindow")
select element:          key(ctrl-shift-c)

please [<user.text>]$:
    user.vscode("workbench.action.showCommands")
    insert(user.text or "")