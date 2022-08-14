mode: user.diablo3
-

^command mode$:
    mode.disable("user.diablo3")
    mode.enable("command")


parrot(pop):                user.diablo_primary_attack()
parrot(cluck):              mouse_click(1)
parrot(tsk):                key(w)

# parrot(shush):              print("shush")
# parrot(hiss):               print("hiss")

{user.letter}:              key(letter)
