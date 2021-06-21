app: vscode
-
tag(): user.ide

# Language features
suggest param:             user.vscode("editor.action.triggerParameterHints")
imports organize:          user.vscode("editor.action.organizeImports")
problem next:              user.vscode("editor.action.marker.nextInFiles")
problem last:              user.vscode("editor.action.marker.prevInFiles")
problem fix:               user.vscode("problems.action.showQuickFixes")
rename it:                 user.vscode("editor.action.rename")
refactor it:               user.vscode("editor.action.refactor")
whitespace trim:           user.vscode("editor.action.trimTrailingWhitespace")

# Split
group <number>:            key("ctrl-{number}")
split right:               user.vscode("workbench.action.splitEditorRight")
split down:                user.vscode("workbench.action.splitEditorDown")

# Sidebar
bar explorer:              user.vscode("workbench.view.explorer")
bar extensions:            user.vscode("workbench.view.extensions")
bar outline:               user.vscode("outline.focus")
bar run:                   user.vscode("workbench.view.debug")
bar search:                user.vscode("workbench.view.search")
bar source:                user.vscode("workbench.view.scm")
bar (show | hide):         user.vscode("workbench.action.toggleSidebarVisibility")

# Panels
panel (show | hide):       user.vscode("workbench.action.togglePanel")
panel control:             user.vscode("workbench.panel.repl.view.focus")
panel output:              user.vscode("workbench.panel.output.focus")
panel problems:            user.vscode("workbench.panel.markers.view.focus")
panel terminal:            user.vscode("workbench.action.terminal.focus")
panel debug:               user.vscode("workbench.debug.action.toggleRepl")
focus editor:              user.vscode("workbench.action.focusActiveEditorGroup")

# Files / Folders
folder add:                user.vscode("workbench.action.addRootFolder")
folder new:                user.vscode("explorer.newFolder")
file new:                  user.vscode("explorer.newFile")
file open folder:          user.vscode("revealFileInOS")
file copy path:            user.vscode("copyFilePath")

# Folding
fold that:                 user.vscode("editor.fold")
unfold that:               user.vscode("editor.unfold")
fold recursive:            user.vscode("editor.foldAllMarkerRegions")
unfold recursive:          user.vscode("editor.unfoldRecursively")
fold all:                  user.vscode("editor.foldAll")
unfold all:                user.vscode("editor.unfoldAll")
fold comments:             user.vscode("editor.foldAllBlockComments")

# Navigation
go back:                   user.vscode("workbench.action.navigateBack")
go forward:                user.vscode("workbench.action.navigateForward")

# Misc
install extension:         user.vscode("workbench.extensions.action.installVSIX")
minimap (show | hide):     user.vscode("editor.action.toggleMinimap")
show settings:             user.vscode("workbench.action.openGlobalSettings")
do command [<user.text>]:
	user.vscode("workbench.action.showCommands")
	insert(user.text or "")