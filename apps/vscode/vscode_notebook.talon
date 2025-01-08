tag: user.vscode_notebook
-

render every cell:          user.run_rpc_command("notebook.renderAllMarkdownCells")

# Execution
run cell:                   user.run_rpc_command("notebook.cell.execute")
run new:                    user.run_rpc_command("notebook.cell.executeAndInsertBelow")
stop cell:                  user.run_rpc_command("notebook.cell.cancelExecution")

# Edit
chuck cell:                 user.run_rpc_command("notebook.cell.delete")
cut cell:                   user.run_rpc_command("notebook.cell.cut")
copy cell:                  user.run_rpc_command("notebook.cell.copy")
paste cell:                 user.run_rpc_command("notebook.cell.paste")
center cell:                user.run_rpc_command("notebook.centerActiveCell")

# Conversion
cell is code:               user.run_rpc_command("notebook.cell.changeToCode")
cell is mark:               user.run_rpc_command("notebook.cell.changeToMarkdown")
cell show numbers:          user.run_rpc_command("notebook.cell.toggleLineNumbers")

# Navigation
cell top:                   user.run_rpc_command("notebook.focusTop")
cell up:                    user.run_rpc_command("notebook.focusPreviousEditor")
cell down:                  user.run_rpc_command("notebook.focusNextEditor")
cell bottom:                user.run_rpc_command("notebook.focusBottom")

# Merging and splitting
cell join above:            user.run_rpc_command("notebook.cell.joinAbove")
cell join below:            user.run_rpc_command("notebook.cell.joinBelow")
cell split:                 user.run_rpc_command("notebook.cell.split")

# Insertion and duplication
drink cell:
    user.run_rpc_command("notebook.cell.insertCodeCellAboveAndFocusContainer")
    user.run_rpc_command("notebook.cell.edit")
pour cell:
    user.run_rpc_command("notebook.cell.insertCodeCellBelowAndFocusContainer")
    user.run_rpc_command("notebook.cell.edit")
clone cell:
    user.run_rpc_command("notebook.cell.copyDown")
    user.run_rpc_command("notebook.cell.edit")
clone cell up:
    user.run_rpc_command("notebook.cell.copyUp")
    user.run_rpc_command("notebook.cell.edit")

# cell view input/output
fold cell:                  user.run_rpc_command("notebook.cell.collapseCellInput")
unfold cell:                user.run_rpc_command("notebook.cell.expandCellInput")
fold every cell:            user.run_rpc_command("notebook.cell.collapseAllCellInputs")
unfold every cell:          user.run_rpc_command("notebook.cell.expandAllCellInputs")

# Output
chuck output:               user.run_rpc_command("notebook.cell.clearOutputs")
chuck every output:         user.run_rpc_command("notebook.clearAllCellsOutputs")
fold output:                user.run_rpc_command("notebook.cell.collapseCellOutput")
unfold output:              user.run_rpc_command("notebook.cell.expandCellOutput")
fold every output:          user.run_rpc_command("notebook.cell.collapseAllCellOutputs")
unfold every output:        user.run_rpc_command("notebook.cell.expandAllCellOutputs")
