tag: user.vscode_notebook
-

render markdown:       user.vscode("notebook.renderAllMarkdownCells")

run stay:              user.vscode("notebook.cell.executeAndFocusContainer")
run new:               user.vscode("notebook.cell.executeAndInsertBelow")
run down:              user.vscode("notebook.cell.executeAndSelectBelow")

chuck cell:            user.vscode("notebook.cell.delete")
cut cell:              user.vscode("notebook.cell.cut")
copy cell:             user.vscode("notebook.cell.copy")
paste cell:            user.vscode("notebook.cell.paste")
center cell:           user.vscode("notebook.centerActiveCell")

chuck output:          user.vscode("notebook.cell.clearOutputs")
fold output:           user.vscode("notebook.cell.collapseCellOutput")
unfold output:         user.vscode("notebook.cell.expandCellOutput")
fold every output:     user.vscode("notebook.cell.collapseAllCellOutputs")
unfold every output:   user.vscode("notebook.cell.expandAllCellOutputs")

clone cell:
    user.vscode("notebook.cell.copyDown")
    user.vscode("notebook.cell.edit")
clone cell up:
    user.vscode("notebook.cell.copyUp")
    user.vscode("notebook.cell.edit")
