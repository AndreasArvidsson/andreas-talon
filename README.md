# Andreas Talon user scripts

All the scripts in my Talon user directory.

In constant development. Things will break!

## Interesting features

This is a list of features that I have implemented that I think is of more interest to other Talon users. Things I have already upstreamed to [knausj](https://github.com/knausj85/knausj_talon) are omitted. Since I don't actually use a fork of knausj some modifications (often different names) might be required.

1. **RePhrase** - Reevaluate spoken phrase after Talon context change. Can for example be used to change to another application/window and execute commands to that window in the same utterance. `"focus firefox tab new"`
   - [window_management.talon](https://github.com/AndreasArvidsson/andreas-talon/blob/f84a1aed3a11608eafcacd12ce37244a6cc07502/misc/window_management/window_management.talon#L1-L5)
   - [window_focus.py](https://github.com/AndreasArvidsson/andreas-talon/blob/f84a1aed3a11608eafcacd12ce37244a6cc07502/misc/window_management/window_focus.py#L111-L117)
   - [rephrase.py](https://github.com/AndreasArvidsson/andreas-talon/blob/4e1dca1ffabf1e119281265fad0c0229ab38b697/misc/rephrase.py)
1. **Custom subtitles** - User customizable subtitles for Talon
   - [on_phrase.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/misc/on_phrase.py)
   - [screen.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/misc/screen.py#L39-L42)
1. **Scroll on hiss noise** - Use the Talon hiss noise to scroll
   - [on_hiss.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/misc/on_hiss.py)
   - [mouse.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/misc/mouse/mouse.py#L97-L112)
1. **Wake Talon on double pop noise** - When Talon is in sleep mode a rapid double pop noise will wake Talon
   - [on_pop.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/misc/on_pop.py)
   - [sleep.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/misc/sleep/sleep.py#L23-L29)
1. **<user.text> with abbreviations, spelling and numbers** - `"say foo numb forty four brief address spell air bat cap bar"` => `foo 44 addr abc bar`
   - [dictation.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/text/dictation.py#L46-L67)
1. **Clipboard manager** - Clipboard manager built in Talon
   - [clipboard_manager.talon](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/misc/clipboard_manager/clipboard_manager.talon)
   - [clipboard_manager.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/misc/clipboard_manager/clipboard_manager.py)
1. **Lorem ipsum generator** - `"lorem ipsum thirty"` => `Lorem ipsum dolor sit amet...`
   - [lorem_ipsum.talon](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/misc/lorem_ipsum/lorem_ipsum.talon)
   - [lorem_ipsum.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/misc/lorem_ipsum/lorem_ipsum.py)
1. **Emoticons insertion** - `"face smile"` => `:)`
   - [emoticons.talon](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/misc/emoticons/emoticons.talon)
   - [emoticons.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/misc/emoticons/emoticons.py)
1. **Snippet insertion** - Generic textual snippet support with override for VSCode
   - [javascript.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/langs/javascript/javascript.py#L139-L144)
   - [snippets.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/text/snippets.py)
1. **Imports fix** - Add missing and remove unused imports for VSCode
   - [vscode.talon](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/apps/vscode/vscode.talon#L31-L34)
   - [vscode.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/apps/vscode/vscode.py#L391-L396)
1. **Copy command ID** - Copy command ID for the selected command in the VSCode command palatte
   - [vscode.talon](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/apps/vscode/vscode.talon#L252)
   - [vscode.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/apps/vscode/vscode.py#L382-L389)
1. **Cursorless integration with VSCode next find match** - `"change blue air three times"`
   - [vscode_take_word.talon](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/apps/vscode/vscode_take_word.talon)
   - [vscode.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/apps/vscode/vscode.py#L340-L348)
   - [repeater.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/misc/repeater/repeater.py#L16-L21)
1. **Foot switch support** - Add support for scrolling, navigating and more
   - [foot_switch.talon](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/misc/foot_switch/foot_switch.talon)
   - [foot_switch.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/misc/foot_switch/foot_switch.py)

## Dependencies

- [Talon Voice](https://talonvoice.com) - The software that makes it all happen
- [Andreas VSCode Talon extension](https://github.com/AndreasArvidsson/vscode-talon-extension) - My own VSCode extension that adds multiple features for using VSCode with Talon
- [Command server](https://marketplace.visualstudio.com/items?itemName=pokey.command-server) - VSCode command API/RPC
- [nircmd](https://www.nirsoft.net/utils/nircmd.html) - Change playback device on windows
- [clipboard-cli](https://www.npmjs.com/package/clipboard-cli) - CLI copy/paste
