app: vscode
win.file_ext: .bashbook
-

tag(): user.vscode_notebook

run take:     user.vscode("bashbook.cell.executeAndSelect")
run clear:    user.vscode("bashbook.cell.executeAndClear")
clear cell:   user.vscode("bashbook.cell.clearAndEdit")