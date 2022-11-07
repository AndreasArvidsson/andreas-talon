tag: user.operators
-

# ----- Assignment operator -----
op (assign | equals):       user.op_assign()

# ----- Math operators -----
op (minus | sub):           user.op_sub()
op (minus | sub) assign:    user.op_sub_assign()
op (plus | add):            user.op_add()
op (plus | add) assign:     user.op_add_assign()
op (multiply | mult):       user.op_mult()
op (multiply | mult) assign: user.op_mult_assign()
op (divide | div):          user.op_div()
op (divide | div) assign:   user.op_div_assign()
op (modulo | mod):          user.op_mod()
op (modulo | mod) assign:   user.op_mod_assign()
op (power | pow):           user.op_exp()

# ----- Comparison operators -----
is equal:                   user.op_equal()
is not equal:               user.op_not_equal()
is less:                    user.op_less()
is greater:                 user.op_greater()
is less [or] equal:         user.op_less_or_eq()
is greater [or] equal:      user.op_greater_or_eq()
is not:                     user.op_not()

is [equal] null:            user.op_equal_null()
is not [equal] null:        user.op_not_equal_null()

# ----- Logical operators -----
op and:                     user.op_and()
op or:                      user.op_or()
