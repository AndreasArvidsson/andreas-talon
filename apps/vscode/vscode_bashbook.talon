app: vscode
win.file_ext: .bashbook
-

tag(): user.vscode_notebook

open as markdown:           user.vscode("bashbook.openNotebookAsMarkdown")
open every output:          user.vscode("bashbook.openAllOutputsInNewFile")
run take:                   user.vscode("bashbook.cell.executeAndSelect")
run clear:                  user.vscode("bashbook.cell.executeAndClear")
run down:                   user.vscode("bashbook.cell.executeWithMarkdownOutput")
clear cell:                 user.vscode("bashbook.cell.clearAndEdit")
copy output:                user.vscode("bashbook.cell.copyOutput")
open output:                user.vscode("bashbook.cell.openOutputInNewFile")
