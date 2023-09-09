tag: terminal
-
tag(): user.file_manager
tag(): user.git
tag(): user.maven
tag(): user.npm
tag(): user.yarn
tag(): user.pip
tag(): user.insert_paste_disabled

vscode install:             "vsce package -o bundle.vsix && code --install-extension bundle.vsix --force\n"

vscode package:             "vsce package\n"

talon user update:
    "find {user.talon_user()} -type d -name .git -print -execdir git pull --ff-only \\;\n"
    "git -C {user.user_home()}/repositories/cursorless-talon pull\n"

watch talon log:            "tail -f {user.talon_home()}/talon.log\n"

run talon deck:             "talon-deck\n"

python version:             "python --version\n"
java version:               "java --version\n"
