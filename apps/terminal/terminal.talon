tag: terminal
-
tag(): user.file_manager
tag(): user.git
tag(): user.maven
tag(): user.npm
tag(): user.yarn

vscode install:
    "vsce package -o bundle.vsix && code --install-extension bundle.vsix --force\n"

vscode package:
    "vsce package\n"

talon user updates:
    "node {user.talon_user()}/andreas/update.js\n"
