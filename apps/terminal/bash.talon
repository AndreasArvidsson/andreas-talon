tag: user.bash
-

cd:                            "cd "
cd <user.text>$:               "cd {text}"
go home:                       "cd ~\n"

list:                          "ls\n"
list all:                      "ls -a\n"
list long:                     "ls -lah\n"
list long pipe:                "ls -lah | "

history:                       "history "
history tail:                  "history | tail\n"
history tail <number_small>:   "history | tail -{number_small}\n"
history grep:                  "history | grep "
run history <number>:          "!{number}\n"
run last:                      "!!\n"
run last <number>:             "!-{number}\n"

head <number_small>:           "head -{number_small}"

tail <number_small>:           "tail -{number_small}"
# watch talon log:               "tail -f {user.talon_home()}/talon.log\n"
watch talon log:               user.tail_talon_log()

print dir:                     "pwd\n"
copy dir:                      "pwd | clipboard\n"

tar create:                    "tar -czvf "
tar extractf:                  "tar -xzvf "

echo:                          "echo "
echo <user.text>$:             "echo {text}"

grep:                          "grep "
make dir:                      "mkdir "
move:                          "mv "
remove:                        "rm "
copy:                          "cp "
less:                          "less "
sudo:                          "sudo "
apt install:                   "apt install "
apt update:                    "apt update\n"
word count:                    "wc "
change mode:                   "chmod "
change owner:                  "chown "
exargs:                        "xargs "
exec:                          "exec "
cat:                           "cat "
diff:                          "diff "
unique:                        "uniq "
clipboard:                     "clipboard"
translate:                     "tr "
vim:                           "vim "
curl:                          "curl "
yarn:                          "yarn "
dev null:                      "/dev/null"
print exit code:               "echo $?\n"
pipe:                          " | "
op and:                        " && "
op or:                         " || "
terminate:                     key(ctrl-c)
clear:                         key(ctrl-l)
revert:                        key(alt-r)

# head:                          "head "
# tail:                          "tail "
# find:                          "find "
# sed:                           "sed "
# set:                           "set "
# ctrl-
# find -exec grep \;
# locate
# echo hello >> myfile.text
# pushd https://linuxhint.com/bash_pushd_command/
# cat /etc/os-release
#cat /proc/version
# fc last command in editor.