tag: user.bash
-

cd [<word>]:                   "cd {word or ''}"
go home:                       "cd ~\n"

list:                          "ls\n"
list all:                      "ls -a\n"
list long:                     "ls -lah\n"
list long pipe:                "ls -lah | "

history:                       "history "
history tail:                  "history | tail\n"
history tail <number_small>:   "history | tail -{number_small}\n"
history grep [<word>]:         "history | grep {word or ''}"
run history <number>:          "!{number}\n"
run last:                      "!!\n"
run last <number>:             "!-{number}\n"

head <number_small>:           "head -{number_small}"

tail <number_small>:           "tail -{number_small}"
watch talon log:               "tail -f {path.talon_home()}/talon.log\n"

print dir:                     "pwd\n"
copy dir:                      "pwd | clipboard\n"

tar create [<word>]:           "tar -czvf {word or ''}"
tar extract [<word>]:          "tar -xzvf {word or ''}"

echo [<user.text>]:            "echo {text or ''}"
grep [<word>]:                 "grep {word or ''}"
make dir [<word>]:             "mkdir {word or ''}"
move:                          "mv "
remove [<word>]:               "rm {word or ''}"
copy:                          "cp "
less:                          "less "
sudo:                          "sudo "
word count:                    "wc "
change mode:                   "chmod "
change owner:                  "chown "
exargs:                        "xargs "
find [<word>]:                 "find {word or ''}"
exec:                          "exec "
cat:                           "cat "
tar:                           "tar "
diff:                          "diff "
unique:                        "uniq "
clipboard:                     "clipboard"
translate:                     "tr "
vim:                           "vim "
curl:                          "curl "
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