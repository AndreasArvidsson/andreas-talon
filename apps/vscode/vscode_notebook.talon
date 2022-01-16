tag: user.vscode_notebook
-

render every cell0:    user.vscode("notebook.renderAllMarkdownCells")

# Execution
run cell:              user.vscode("notebook.cell.execute")
run new:               user.vscode("notebook.cell.executeAndInsertBelow")
stop cell:             user.vscode("notebook.cell.cancelExecution")

# Edit
chuck cell:            user.vscode("notebook.cell.delete")
cut cell:              user.vscode("notebook.cell.cut")
copy cell:             user.vscode("notebook.cell.copy")
paste cell:            user.vscode("notebook.cell.paste")
center cell:           user.vscode("notebook.centerActiveCell")

# Conversion
cell is code:          user.vscode("notebook.cell.changeToCode")
cell is mark:          user.vscode("notebook.cell.changeToMarkdown")
cell show numbers:     user.vscode("notebook.cell.toggleLineNumbers")

# Navigation
cell top:              user.vscode("notebook.focusTop")
cell up:               user.vscode("notebook.focusPreviousEditor")
cell down:             user.vscode("notebook.focusNextEditor")
cell bottom:           user.vscode("notebook.focusBottom")

# Merging and splitting
cell join above:       user.vscode("notebook.cell.joinAbove")
cell join below:       user.vscode("notebook.cell.joinBelow")
cell split:            user.vscode("notebook.cell.split")

# Insertion and duplication
drink cell:
    user.vscode("notebook.cell.insertCodeCellAboveAndFocusContainer")
    user.vscode("notebook.cell.edit")
pour cell:
    user.vscode("notebook.cell.insertCodeCellBelowAndFocusContainer")
    user.vscode("notebook.cell.edit")
clone cell:
    user.vscode("notebook.cell.copyDown")
    user.vscode("notebook.cell.edit")
clone cell up:
    user.vscode("notebook.cell.copyUp")
    user.vscode("notebook.cell.edit")

# cell view input/output
fold cell:             user.vscode("notebook.cell.collapseCellInput")
unfold cell:           user.vscode("notebook.cell.expandCellInput")
fold every cell:       user.vscode("notebook.cell.collapseAllCellInputs")
unfold every cell:     user.vscode("notebook.cell.expandAllCellInputs")

# Output
chuck output:          user.vscode("notebook.cell.clearOutputs")
chuck every output:    user.vscode("notebook.clearAllCellsOutputs")
fold output:           user.vscode("notebook.cell.collapseCellOutput")
unfold output:         user.vscode("notebook.cell.expandCellOutput")
fold every output:     user.vscode("notebook.cell.collapseAllCellOutputs")
unfold every output:   user.vscode("notebook.cell.expandAllCellOutputs")