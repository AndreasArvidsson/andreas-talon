tag: user.ide
-
tag(): user.zoom
tag(): user.tabs

# ----- Navigation -----
declaration go:                user.declaration_go()
definition go:                 user.definition_go()
definition peek:               user.definition_peek()
definition split:              user.definition_split()
references go:                 user.references_go()
references peek:               user.references_peek()

# ----- Line commands -----
go <number>:                   edit.jump_line(number)
head <number>:                 user.line_start(number)
tail <number>:                 user.line_end(number)
middle <number>:               user.line_middle(number)

select <number>:               edit.select_line(number)
go <number> extend <number>:   edit.select_lines(number_1, number_2)
extend <number>:               edit.extend_line(number)

scratch <number>:              user.delete_line(number)
cut <number>:                  user.cut_line(number)
copy <number>:                 user.copy_line(number)
(clone | dupe) <number>:       user.clone_line(number)

# ----- Format -----
format document:               user.format_document()
format it:                     user.format_selection()

# ----- Comments -----
comment it:                    user.comment()
uncomment it:                  user.uncomment()

# ----- Run and debug -----
run program:                   user.run_program()
debug program:                 user.debug_program()
breakpoint:                    user.debug_breakpoint()
continue:                      user.debug_continue()
step over:                     user.debug_step_over()
step into:                     user.debug_step_into()
step out:                      user.debug_step_out()
restart:                       user.debug_restart()
pause:                         user.debug_pause()
stop:                          user.debug_stop()

# ----- Misc -----
quick fix:                     user.quick_fix()
suggest:                       code.complete()