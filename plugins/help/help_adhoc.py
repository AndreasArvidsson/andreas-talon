from talon import scope, app, registry
from ...core.imgui import imgui


def get_list(name):
    l = list(scope.get(name))
    l.sort()
    return ", ".join(l)


command_key = "___lpcommand__mode___pi__over___pi___c3_b6ver_rp_ra__"


@imgui.open(x=0, y=0)
def gui(gui: imgui.GUI):
    gui.text(get_list("mode"))
    gui.text(get_list("language"))
    gui.text(scope.get("speech.engine"))
    gui.text("över: yes" if command_key in registry.commands else "över: no")


# sim("över")

# print(registry.commands)

#  {
#  '___ltuser_2eprose_gt__': [CommandImpl('<user.prose>')],
#  '___la_lplistpunkt___pi__list__punkt_rp__': [CommandImpl('(listpunkt | list punkt)')],
#  '___lauppgift__': [CommandImpl('uppgift')],
#  '___la_lpindrag___pi__in__drag_rp__': [CommandImpl('(indrag | in drag)')],
#  '___lautdrag__': [CommandImpl('utdrag')],
#  '___lpny___pi__nu_rp__rad__': [CommandImpl('(ny | nu) rad')],
#  '___lpny___pi__nu_rp___lpparagraf___pi__graf_rp__': [CommandImpl('(ny | nu) (paragraf | graf)')],
#  '___lpcommand__mode___pi__over___pi___c3_b6ver_rp_ra__': [CommandImpl('(command mode | over | över)')],
#  '___lbuser_2esleep_5fphrase_rb___ls_ltphrase_gt_rs_ra__': [CommandImpl('{user.sleep_phrase} [<phrase>]')],
#  '___lbuser_2eabort_5fphrase_rb_ra__': [CommandImpl('{user.abort_phrase}')]
#  }
