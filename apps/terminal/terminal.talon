tag: terminal
-

tag(): user.file_manager
tag(): user.git
tag(): user.maven
tag(): user.npm
tag(): user.yarn
tag(): user.pip
tag(): user.docker
tag(): user.ollama
tag(): user.codex_cli
tag(): user.insert_paste_disabled

vscode install:             "vsce package -o bundle.vsix && code --install-extension bundle.vsix --force\n"

vscode package:             "vsce package\n"

run talon deck:             "talon-deck\n"

python version:             "python --version\n"
java version:               "java --version\n"

pre commit version:         "pre-commit --version\n"
pre commit install:         "pre-commit install\n"
pre commit uninstall:       "pre-commit uninstall\n"
pre commit run:             "pre-commit run --all-files\n"
