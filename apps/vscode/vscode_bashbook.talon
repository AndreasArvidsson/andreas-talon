app: vscode
win.file_ext: .bashbook
-

tag(): user.vscode_notebook

open as markdown:           user.run_rpc_command("bashbook.openNotebookAsMarkdown")
open every output:          user.run_rpc_command("bashbook.openAllOutputsInNewFile")
run take:                   user.run_rpc_command("bashbook.cell.executeAndSelect")
run clear:                  user.run_rpc_command("bashbook.cell.executeAndClear")
run down:                   user.run_rpc_command("bashbook.cell.executeWithMarkdownOutput")
clear cell:                 user.run_rpc_command("bashbook.cell.clearAndEdit")
copy output:                user.run_rpc_command("bashbook.cell.copyOutput")
open output:                user.run_rpc_command("bashbook.cell.openOutputInNewFile")
