tag: user.operators
-

# ----- Assignment operator -----
op assign:                      user.op_assign()

# ----- Math operators -----
op (minus | sub):               user.op_sub()
op (minus | sub) assign:        user.op_sub_assign()
op (plus | add):                user.op_add()
op (plus | add) assign:         user.op_add_assign()
op (multiply | mult):           user.op_mult()
op (multiply | mult) assign:    user.op_mult_assign()
op (divide | div):              user.op_div()
op (divide | div) assign:       user.op_div_assign()
op (modulo | mod):              user.op_mod()
op (modulo | mod) assign:       user.op_mod_assign()
op (power | pow):               user.op_exp()

# ----- Comparison operators -----
(op | is) equal:                user.op_equal()
(op | is) not equal:            user.op_not_equal()
(op | is) less:                 user.op_less()
(op | is) greater:              user.op_greater()
(op | is) less [or] equal:      user.op_less_or_eq()
(op | is) greater [or] equal:   user.op_greater_or_eq()
(op | is) not:                  user.op_not()

# ----- Logical operators -----
op and:                         user.op_and()
op or:                          user.op_or()