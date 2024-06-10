tag: terminal
-
tag(): user.file_manager
tag(): user.git
tag(): user.maven
tag(): user.npm
tag(): user.yarn
tag(): user.pip

vscode install:             "vsce package -o bundle.vsix && code --install-extension bundle.vsix --force\n"

vscode package:             "vsce package\n"

run talon deck:             "talon-deck\n"

python version:             "python --version\n"
java version:               "java --version\n"
