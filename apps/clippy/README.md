# Clippy

Clipboard manager with RPC and Talon support. Supports copying and pasting multiple things at once.

## Installation

1. Copy this folder to your Talon user directory
2. Install the Clippy application
    - https://github.com/AndreasArvidsson/clippy

## Command examples

For all commands look in:  
[clippy.talon](./clippy.talon)

### Without a target

-   `"clippy"` to show/hide Clippy UI
-   `"clippy search"` to show/hide search input
-   `"clippy dev tools"` to show/hide developer tools

For list of Clippy commands without a target:  
[clippy_command_no_targets.talon-list](./clippy_command_no_targets.talon-list)

### Single target

-   `"clippy copy 1"`
    -   Copy item `1`
-   `"clippy paste air"`
    -   Paste item `a`
-   `"clippy chuck a"`
    -   Remove item `a`

For list of Clippy commands with one or multiple targets:  
[clippy_command_with_targets.talon-list](./clippy_command_with_targets.talon-list)

### Multiple targets

-   `"clippy copy air and bat"`
    -   Copy items `a` and `b`
-   `"clippy copy air past bat"`
    -   Copy items in the range `a` through `b`
-   `"clippy copy 2 items air"`
    -   Copy two items: `a` and the one below
-   `"clippy copy 2 items reverse air"`
    -   Copy two items: `a` and the one below in reverse order

### Paste only shorthands

These are only supported for the paste action and mostly used when Clippy is hidden

-   `"paste 2 items"`
    -   Paste the first (last copied) two items in reverse order
-   `"paste second"`
    -   Paste second (2) clipboard item
-   `"paste first and second"`
    -   Paste first (1) and second (2) clipboard items

## Images

![Clippy](./clippy.png)
