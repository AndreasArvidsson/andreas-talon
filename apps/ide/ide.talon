tag: user.ide
-
tag(): user.zoom
tag(): user.tabs
tag(): user.find

# ----- Navigation -----
# declaration go:            user.declaration_go()
# definition go:             user.definition_go()
# definition peek:           user.definition_peek()
# definition split:          user.definition_split()
# references go:             user.references_go()
# references peek:           user.references_peek()

# ----- Line commands -----
go line <number>:          edit.jump_line(number)
# pre row <number>:          user.line_start(number)
# post row <number>:         user.line_end(number)
# middle row <number>:       user.line_middle(number)

# take row <number>:         edit.select_line(number)
# take row <number> past <number>:
#     edit.select_lines(number_1, number_2)
# extend row <number>:       edit.extend_line(number)

# TODO
# chuck line <number>:       user.delete_line(number)
# cut line <number>:         user.cut_line(number)
# copy line <number>:        user.copy_line(number)
# dupe line <number>:        user.clone_line(number)

# ----- Format -----
format document:           user.format_document()
# format (this | dis):       user.format_selection()

# ----- Comments -----
# comment:                   user.comment()
# uncomment:                 user.uncomment()
# comment:                   code.toggle_comment()

# ----- Run and debug -----
run program:               user.run_program()
debug (program | start):   user.debug_program()
breakpoint:                user.debug_breakpoint()
continue:                  user.debug_continue()
step over:                 user.debug_step_over()
step into:                 user.debug_step_into()
step out:                  user.debug_step_out()
debug restart:             user.debug_restart()
debug pause:               user.debug_pause()
debug stop:                user.debug_stop()

# ----- Misc -----
# quick fix:                 user.quick_fix()
suggest:                   code.complete()