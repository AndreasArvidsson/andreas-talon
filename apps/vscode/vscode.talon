app: vscode
-
tag(): user.ide
tag(): user.scroll
tag(): user.cursorless_experimental_snippets
tag(): user.navigation

settings():
    user.scroll_step = 600

# Language features
suggest param:               user.vscode("editor.action.triggerParameterHints")
imports organize:            user.vscode("editor.action.organizeImports")
problem next:                user.vscode("editor.action.marker.nextInFiles")
problem last:                user.vscode("editor.action.marker.prevInFiles")
problem fix:                 user.vscode("problems.action.showQuickFixes")
refactor this:               user.vscode("editor.action.refactor")

ref next:
    user.vscode("references-view.tree.focus")
    key(down enter)
ref last:
    user.vscode("references-view.tree.focus")
    key(up enter)

# Split
split up:                    user.vscode("workbench.action.moveEditorToAboveGroup")
split down:                  user.vscode("workbench.action.moveEditorToBelowGroup")
split left:                  user.vscode("workbench.action.moveEditorToLeftGroup")
split right:                 user.vscode("workbench.action.moveEditorToRightGroup")
focus up:                    user.vscode("workbench.action.focusAboveGroup")
focus down:                  user.vscode("workbench.action.focusBelowGroup")
focus left:                  user.vscode("workbench.action.focusLeftGroup")
focus right:                 user.vscode("workbench.action.focusRightGroup")
split flip:                  user.vscode("workbench.action.toggleEditorGroupLayout")
split clear:                 user.vscode("workbench.action.joinTwoGroups")
split clear all:             user.vscode("workbench.action.editorLayoutSingle")
cross:                       user.vscode("workbench.action.focusNextGroup")
open cross:                  key(ctrl-enter)

# Sidebar
bar (show | hide):           user.vscode("workbench.action.toggleSidebarVisibility")
bar explorer:                user.vscode("workbench.view.explorer")
bar extensions:              user.vscode("workbench.view.extensions")
bar outline:                 user.vscode("outline.focus")
bar debug:                   user.vscode("workbench.view.debug")
bar search:                  user.vscode("workbench.view.search")
bar source:                  user.vscode("workbench.view.scm")
bar file:                    user.vscode("workbench.files.action.showActiveFileInExplorer")
search last:                 user.vscode("search.action.focusPreviousSearchResult")
search next:                 user.vscode("search.action.focusNextSearchResult")

# Panel
panel (show | hide):         user.vscode("workbench.action.togglePanel")
panel (large | small):       user.vscode("workbench.action.toggleMaximizedPanel")
panel control:               user.vscode("workbench.panel.repl.view.focus")
panel output:                user.vscode("workbench.panel.output.focus")
panel problems:              user.vscode("workbench.panel.markers.view.focus")
panel terminal:              user.vscode("workbench.action.terminal.focus")
panel debug:                 user.vscode("workbench.debug.action.toggleRepl")
panel clear:                 user.vscode("workbench.debug.panel.action.clearReplAction")

# Focus editor
focus editor:                user.vscode("workbench.action.focusActiveEditorGroup")

# Hide sidebar and panel
hide all:
    user.vscode("workbench.action.closeSidebar")
    user.vscode("workbench.action.closePanel")

# Files / Folders
folder open:                 user.vscode("workbench.action.files.openFolder")
folder add:                  user.vscode("workbench.action.addRootFolder")
folder new:                  user.vscode("explorer.newFolder")
file open:                   user.vscode("workbench.action.files.openFile")
file new:                    user.vscode("explorer.newFile")
file open folder:            user.vscode("revealFileInOS")
file copy path:              user.vscode("copyFilePath")
file open git:               user.git_open_working_file()

# Folding
fold that:                   user.vscode("editor.fold")
unfold that:                 user.vscode("editor.unfold")
fold recursive:              user.vscode("editor.foldAllMarkerRegions")
unfold recursive:            user.vscode("editor.unfoldRecursively")
fold all:                    user.vscode("editor.foldAll")
unfold all:                  user.vscode("editor.unfoldAll")
fold comments:               user.vscode("editor.foldAllBlockComments")

# Navigation
take next:                   user.vscode("editor.action.addSelectionToNextFindMatch")
take last:                   user.vscode("editor.action.addSelectionToPreviousFindMatch")
take all these:              user.vscode("editor.action.selectHighlights")
cursor back:                 user.vscode("cursorUndo")
cursor forward:              user.vscode("cursorRedo")

# Debug
debug select:                user.vscode("workbench.action.debug.selectandstart")
debug extension:
    user.vscode("workbench.action.debug.selectandstart")
    "run extension"
    key(enter)
debug test:
    user.vscode("workbench.action.debug.selectandstart")
    "extension tests"
    key(enter)
dev tools:                   user.vscode("workbench.action.toggleDevTools")
select element:              key(ctrl-shift-c)

# Find session
scout sesh [<user.text>]$:   user.vscode_find_recent(text or "")
pop sesh <user.text>$:
    user.vscode_find_recent(text)
    key(enter)
pop sesh:
    user.vscode_find_recent("", 1)
    key(enter)

# Misc
install extension:           user.vscode("workbench.extensions.action.installVSIX")
minimap (show | hide):       user.vscode("editor.action.toggleMinimap")
reload window:               user.vscode("workbench.action.reloadWindow")
open settings json:          user.vscode("workbench.action.openSettingsJson")
zen mode:                    user.vscode("workbench.action.toggleZenMode")
next:                        user.vscode("jumpToNextSnippetPlaceholder")
cursorless record:           user.vscode("cursorless.recordTestCase")

please [<user.text>]$:
    user.vscode("workbench.action.showCommands")
    insert(user.text or "")