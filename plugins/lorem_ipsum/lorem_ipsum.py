from talon import Module, actions

mod = Module()


@mod.action_class
class Actions:
    def lorem_ipsum(num_words: int):
        """Inserts a lorem ipsum with <num_words> words"""
        res = words[:num_words]
        last_word = res[-1]
        if last_word[-1] == ",":
            last_word = last_word[:-1]
        if last_word[-1] != ".":
            last_word += "."
        res[-1] = last_word
        res = " ".join(res)
        actions.insert(res)


lorem_ipsum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Urna nunc id cursus metus. Luctus venenatis lectus magna fringilla urna porttitor rhoncus. Tellus elementum sagittis vitae et leo duis. Diam vulputate ut pharetra sit amet aliquam id diam maecenas. Amet consectetur adipiscing elit ut aliquam. Ut enim blandit volutpat maecenas volutpat blandit aliquam etiam. Maecenas ultricies mi eget mauris pharetra et. Quam vulputate dignissim suspendisse in est ante. Diam phasellus vestibulum lorem sed.

Dui accumsan sit amet nulla. Diam vulputate ut pharetra sit amet aliquam id diam. Sed risus ultricies tristique nulla aliquet enim tortor at. In metus vulputate eu scelerisque felis imperdiet. Viverra tellus in hac habitasse. Viverra tellus in hac habitasse platea dictumst vestibulum rhoncus est. Nisl purus in mollis nunc sed id. Porta nibh venenatis cras sed felis eget velit aliquet. Nisi vitae suscipit tellus mauris a. Cras ornare arcu dui vivamus arcu felis bibendum ut tristique. Phasellus egestas tellus rutrum tellus. Aliquam nulla facilisi cras fermentum odio. Massa eget egestas purus viverra accumsan in nisl. Libero nunc consequat interdum varius sit amet mattis vulputate enim. Sagittis orci a scelerisque purus. Egestas maecenas pharetra convallis posuere morbi leo urna molestie. Eget aliquet nibh praesent tristique magna sit amet. Id faucibus nisl tincidunt eget nullam.

Porttitor eget dolor morbi non arcu risus quis varius quam. Tellus pellentesque eu tincidunt tortor aliquam. Platea dictumst quisque sagittis purus sit amet volutpat consequat. Scelerisque felis imperdiet proin fermentum leo vel orci. Ac auctor augue mauris augue neque gravida in. Proin fermentum leo vel orci. Sit amet purus gravida quis blandit. Sed enim ut sem viverra aliquet eget sit. Dignissim enim sit amet venenatis urna cursus eget nunc scelerisque. A diam maecenas sed enim ut. A diam sollicitudin tempor id eu nisl.

Massa placerat duis ultricies lacus sed turpis tincidunt id. Commodo elit at imperdiet dui accumsan sit amet nulla. Est ante in nibh mauris cursus mattis molestie a. Nullam ac tortor vitae purus faucibus ornare. Orci ac auctor augue mauris. Fermentum posuere urna nec tincidunt praesent semper. Semper auctor neque vitae tempus quam pellentesque nec. Netus et malesuada fames ac turpis egestas. Dolor morbi non arcu risus quis varius. Nec tincidunt praesent semper feugiat nibh sed pulvinar proin gravida. Elit sed vulputate mi sit amet. Dignissim suspendisse in est ante in nibh.

Cras sed felis eget velit aliquet sagittis id consectetur. Varius quam quisque id diam vel quam elementum pulvinar etiam. Venenatis tellus in metus vulputate eu scelerisque felis. In vitae turpis massa sed. Bibendum at varius vel pharetra vel turpis. Morbi tristique senectus et netus et malesuada fames ac. Amet dictum sit amet justo donec enim diam vulputate ut. Placerat orci nulla pellentesque dignissim. Lacus laoreet non curabitur gravida arcu. Ut ornare lectus sit amet. Commodo elit at imperdiet dui accumsan sit. Pulvinar proin gravida hendrerit lectus a. Nec feugiat nisl pretium fusce id velit ut tortor. Diam sollicitudin tempor id eu nisl. Neque convallis a cras semper. Sagittis nisl rhoncus mattis rhoncus urna neque viverra. Aliquam sem et tortor consequat id porta nibh. Consectetur purus ut faucibus pulvinar elementum integer.

Orci ac auctor augue mauris augue neque gravida in fermentum. Dolor sit amet consectetur adipiscing elit pellentesque habitant morbi. Ante metus dictum at tempor commodo ullamcorper a lacus. Morbi leo urna molestie at. Et egestas quis ipsum suspendisse ultrices gravida. Potenti nullam ac tortor vitae purus faucibus. Tempus urna et pharetra pharetra massa massa ultricies mi. Id diam maecenas ultricies mi eget mauris pharetra et. Pellentesque pulvinar pellentesque habitant morbi tristique senectus et netus. Ultricies mi quis hendrerit dolor magna eget. Eget gravida cum sociis natoque penatibus et magnis dis parturient. Quisque non tellus orci ac auctor augue mauris. Leo a diam sollicitudin tempor id eu nisl. In pellentesque massa placerat duis ultricies. Nam at lectus urna duis.

Placerat orci nulla pellentesque dignissim enim sit amet venenatis. Commodo odio aenean sed adipiscing diam. Faucibus vitae aliquet nec ullamcorper sit amet risus nullam. Quis vel eros donec ac odio tempor orci dapibus ultrices. Et netus et malesuada fames. Hendrerit gravida rutrum quisque non tellus. Vitae semper quis lectus nulla at volutpat diam ut venenatis. Morbi tincidunt augue interdum velit euismod. Sagittis orci a scelerisque purus semper eget duis at tellus. Donec ac odio tempor orci dapibus ultrices in iaculis nunc. Montes nascetur ridiculus mus mauris vitae.

Massa sapien faucibus et molestie ac feugiat sed. Orci dapibus ultrices in iaculis nunc. Sit amet luctus venenatis lectus. Arcu non sodales neque sodales. Elit ullamcorper dignissim cras tincidunt lobortis feugiat. Cursus risus at ultrices mi tempus. Vulputate ut pharetra sit amet aliquam id diam maecenas ultricies. Proin sed libero enim sed. Odio aenean sed adipiscing diam donec adipiscing tristique risus. In tellus integer feugiat scelerisque. Vitae nunc sed velit dignissim sodales ut eu sem. Consequat id porta nibh venenatis cras sed felis eget velit. Aliquet enim tortor at auctor urna nunc id cursus metus. Tincidunt ornare massa eget egestas purus viverra accumsan. Nam aliquam sem et tortor consequat id porta nibh venenatis. Interdum posuere lorem ipsum dolor. Vel orci porta non pulvinar neque laoreet suspendisse interdum consectetur."""

words = lorem_ipsum.split(" ")
