# Andreas Talon user scripts

All the scripts in my Talon user directory. These scripts are not based upon Talon community/knausj and are therefore not always compatible with names defined in community. In constant development. Things may break!

> **Note**
> If you find the scripts in this repository helpful, [consider sponsoring](https://github.com/sponsors/AndreasArvidsson)!

## Interesting features

This is a list of features that I have implemented that I think is of more interest to other Talon users. Things I have already upstreamed to [Talon community](https://github.com/talonhub/community) are omitted. Since I don't actually use a fork of community some modifications (often different names) might be required.

1. **VSCode language definition for Talon** - Supports `on hover` and `go to definition` for Talon lists, captures and actions.
    - [andreas-talon-vscode](https://github.com/AndreasArvidsson/andreas-talon-vscode)
2. **Command history** - Improved command history with description of commands
    - [Command history](./core/on_phrase/command_history)
3. **Analyze phrase** - Analyze a Talon phrase and retrieve metadata and description of commands
    - [Analyze phrase](./core/on_phrase/analyze_phrase)
4. **Talon Deck** - Stream deck inspired interactive dashboard for Talon Voice
    - [Talon Deck](https://github.com/AndreasArvidsson/talon-deck)
5. **Clippy - Clipboard manager** - Clipboard manager with Talon rpc support
    - [Clippy](./apps/clippy)
6. **Quick pick** - UI for quick access to useful features by clicking buttons
    - [Quick pick](./plugins/quick_pick)
7. **Foot switch support** - Add support for scrolling, navigating and more
    - [Foot switch](./core/foot_switch)
8. **<user.prose> with abbreviations, spelling and numbers** - `"say foo forty four brief address air bat cap bar"` => `foo 44 addr abc bar`
    - [text_and_dictation.py](https://github.com/AndreasArvidsson/andreas-talon/blob/f46880c3932e43c101fe5b004f1e6edd14262c1b/core/text/text_and_dictation.py#L34-L45)
9. **Smarter homophones** - Talon remembers recently used homophones and automatically replaces/reuses your chosen version
    - [dictation.py](https://github.com/AndreasArvidsson/andreas-talon/blob/b21c9eb553950ff9b3c137a98e8c705a3e8cb393/core/text/text_and_dictation.py#L127)
    - [homophones.py](https://github.com/AndreasArvidsson/andreas-talon/blob/b21c9eb553950ff9b3c137a98e8c705a3e8cb393/core/homophones/homophones.py#L99-L108)
10. **Lorem ipsum generator** - `"lorem ipsum thirty"` => `Lorem ipsum dolor sit amet...`
    - [Lorem ipsum](./plugins/lorem_ipsum)
11. **Imports fix** - Add missing and remove unused imports for VSCode
    - [vscode.talon](https://github.com/AndreasArvidsson/andreas-talon/blob/cc2f5ecd5f696addd1d8df60207337e295fa800e/apps/vscode/vscode.talon#L32-L35)
    - [vscode.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/apps/vscode/vscode.py#L391-L396)
12. **Copy command ID** - Copy command ID for the selected command in the VSCode command palette
    - [vscode.talon](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/apps/vscode/vscode.talon#L252)
    - [vscode.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/apps/vscode/vscode.py#L382-L389)
13. **Wake Talon on double pop noise** - When Talon is in sleep mode a rapid double pop noise will wake Talon
    - [on_pop.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/misc/on_pop.py)
    - [sleep.py](https://github.com/AndreasArvidsson/andreas-talon/blob/ef049e9cf50b2694ee1b2f039fc102bd488ca1ae/misc/sleep/sleep.py#L23-L29)

## Dependencies

-   [Talon Voice](https://talonvoice.com) - The software that makes it all happen
-   [Cursorless](https://github.com/cursorless-dev/cursorless) - Don't even try to edit code without it
-   [Andreas VSCode Talon extension](https://github.com/AndreasArvidsson/vscode-talon-extension) - My own VSCode extension that adds multiple features for using VSCode with Talon
-   [Rango Talon](https://github.com/AndreasArvidsson/rango-talon) - Rango Talon side
-   [Rango extension](https://addons.mozilla.org/en-US/firefox/addon/rango) - Rango extension browser side
-   [Command client](https://github.com/AndreasArvidsson/talon-vscode-command-client) - Command RPC client Talon side
-   [Command server](https://marketplace.visualstudio.com/items?itemName=pokey.command-server) - Command RPC extension VSCode side
-   [nircmd](https://www.nirsoft.net/utils/nircmd.html) - Change playback device on windows
-   [clipboard-cli](https://www.npmjs.com/package/clipboard-cli) - CLI copy/paste
