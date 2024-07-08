type App = any;
type Capture = any;
type CommandImpl = any;
type Image = any;
type Path = any;
type Phrase = any;
type Rect = any;
type ResourceContext = any;
type Screen = any;
type ScriptImpl = any;
type TalonScript = any;
type Window = any;

export interface ActionNamespaces {
    main: {
        /** Apply text formatting, such as auto spacing, for the native language */
        auto_format(text: string): string;
        /** Insert text at the current cursor position, automatically formatting it using the actions.auto_format(text) */
        auto_insert(text: string): void;
        /** Insert text at the current cursor position */
        insert(text: string): void;
        /** Press one or more keys by name, space-separated */
        key(key: string): void;
        /** Simulate speaking {text} */
        mimic(text: string): void;
        /** Press and release a mouse button */
        mouse_click(button?: number): void;
        /** Hold down a mouse button */
        mouse_drag(button?: number): void;
        /** Move mouse to (x, y) coordinate */
        mouse_move(x: number, y: number): void;
        /** Release a mouse button */
        mouse_release(button?: number): void;
        /** Scroll the mouse wheel */
        mouse_scroll(y?: number, x?: number, by_lines?: boolean): void;
        /** Mouse X position */
        mouse_x(): number;
        /** Mouse Y position */
        mouse_y(): number;
        /** Display an object in the log */
        print(obj: any): void;
        /** Do nothing */
        skip(): void;
        /** Pause for some duration.
            If you use a number, it is seconds, e.g 1.5 seconds or 0.001 seconds.
            If you use a string, it is a timespec, such as "50ms" or "10s"
            For performance reasons, sleep() cannot be reimplemented by a Context. */
        sleep(duration: number | string): void;
    };
    app: {
        /** Get active app's bundle identifier */
        bundle(): string;
        /** Get active app's executable name */
        executable(): string;
        /** Get active app's name */
        name(): string;
        /** Show a desktop notification */
        notify(body?: string, title?: string, subtitle?: string, sound?: boolean): void;
        /** Get active app's file path */
        path(): string;
        /** Open app preferences */
        preferences(): void;
        /** Close the current tab */
        tab_close(): void;
        /** Switch to next tab for this window */
        tab_next(): void;
        /** Open a new tab */
        tab_open(): void;
        /** Switch to previous tab for this window */
        tab_previous(): void;
        /** Re-open the last-closed tab */
        tab_reopen(): void;
        /** Close the current window */
        window_close(): void;
        /** Hide the current window */
        window_hide(): void;
        /** Switch to next window for this app */
        window_next(): void;
        /** Open a new window */
        window_open(): void;
        /** Switch to previous window for this app */
        window_previous(): void;
    };
    browser: {
        /** Focus the search box */
        focus_search(): void;
        /** Go to a blank page */
        go_blank(): void;
    };
    bytes: {
        /** Convert bytes to base64 */
        base64(b: Uint8Array): string;
        /** Decode bytes to string */
        decode(b: Uint8Array, encoding?: string, errors?: string): Uint8Array;
        /** Convert base64 to bytes */
        frombase64(s: string): Uint8Array;
        /** Convert hex to bytes */
        fromhex(s: string): Uint8Array;
        /** Convert bytes to hex */
        hex(b: Uint8Array): string;
    };
    clip: {
        /** Send key sequence and return resulting clipboard text */
        capture_text(key: string): void;
        /** Clear clipboard contents */
        clear(): null;
        /** Get clipboard image */
        image(): Image | null;
        /** Set clipboard image */
        set_image(image: Image): void;
        /** Set clipboard text */
        set_text(text: string): void;
        /** Get clipboard text */
        text(): string;
        /** Wait for the clipboard to change */
        wait(fmt?: string, timeout?: number): void;
    };
    code: {
        /** Trigger code autocomplete */
        complete(): void;
        /** Return the active programming language */
        language(): void;
        /** Toggle comments on the current line(s) */
        toggle_comment(): void;
    };
    core: {
        /** Cancel the currently running phrase */
        cancel_phrase__unstable(): void;
        /** Return the currently executing command */
        current_command__unstable(): [CommandImpl, Capture];
        /** Return the last executed command */
        last_command(): [CommandImpl, Capture];
        /** Return the last-spoken phrase */
        last_phrase(): Capture;
        /** Return recently executed commands (grouped by phrase) */
        recent_commands(): [CommandImpl, Capture][][];
        /** Return recently-spoken phrases */
        recent_phrases(): Capture[];
        /** Repeat the last command N times */
        repeat_command(times?: number): void;
        /** Repeat the previous phrase or current partial phrase N times */
        repeat_partial_phrase(times?: number): void;
        /** Repeat the last phrase N times */
        repeat_phrase(times?: number): void;
        /** Replace the current command in history with one or more commands */
        replace_command(commands: [CommandImpl, Capture][]): void;
        /** Run a single command for a recognized phrase */
        run_command(cmd: CommandImpl, m: Capture): void;
        /** Run all commands for a hotkey */
        run_hotkey(hotkey: ScriptImpl): void;
        /** Run all commands for a recognized phrase */
        run_phrase(phrase: Capture): void;
        /** Run a single TalonScript for a recognized phrase */
        run_talon_script(ctx: ResourceContext, script: TalonScript, m: Capture): void;
    };
    dict: {
        /** Clear a dict */
        clear(d: Record<string, any>): null;
        /** Check if key appears in dict */
        contains(d: Record<string, any>, key: any): boolean;
        /** Copy a dict */
        copy(d: Record<string, any>): Record<string, any>;
        /** Get dict[key] */
        get(d: Record<string, any>, key: any, default_?: any): any;
        /** Create an empty dict */
        new(): Record<string, any>;
        /** Remove and return dict[key] */
        pop(d: Record<string, any>, key: any): any;
        /** Set dict[key] = value */
        set(d: Record<string, any>, key: any, value: any): null;
        /** Copy all key/value pairs from b into a */
        update(a: Record<string, any>, b: Record<string, any>): null;
    };
    dictate: {
        /** Join a list of words into a single string for insertion */
        join_words(words: string[], separator?: string): string;
        /** Insert lowercase text with auto_insert() */
        lower(p: Phrase): void;
        /** Insert naturally-capitalized text with auto_insert() */
        natural(p: Phrase): void;
        /** Extract words from a spoken Capture */
        parse_words(p: Phrase): string[];
        /** Replace words according to the dictate.word_map dictionary setting */
        replace_words(words: string[]): string[];
    };
    edit: {
        /** Copy selection to clipboard */
        copy(): void;
        /** Cut selection to clipboard */
        cut(): void;
        /** Delete selection */
        delete(): void;
        /** Delete all text in document */
        delete_all(): void;
        /** Delete line under cursor */
        delete_line(): void;
        /** Delete paragraph under cursor */
        delete_paragraph(): void;
        /** Delete word under cursor */
        delete_word(): void;
        /** Move cursor down one row */
        down(): void;
        /** Extend selection down one row */
        extend_down(): void;
        /** Extend selection to end of file */
        extend_file_end(): void;
        /** Extend selection to start of file */
        extend_file_start(): void;
        /** Extend selection left one column */
        extend_left(): void;
        /** Extend selection down one full line */
        extend_line_down(): void;
        /** Extend selection to end of line */
        extend_line_end(): void;
        /** Extend selection to start of line */
        extend_line_start(): void;
        /** Extend selection up one full line */
        extend_line_up(): void;
        /** Extend selection to the end of the current paragraph */
        extend_paragraph_end(): void;
        /** Extend selection to the start of the current paragraph */
        extend_paragraph_start(): void;
        /** Extend selection right one column */
        extend_right(): void;
        /** Extend selection up one row */
        extend_up(): void;
        /** Extend selection left one word */
        extend_word_left(): void;
        /** Extend selection right one word */
        extend_word_right(): void;
        /** Move cursor to end of file (start of line) */
        file_end(): void;
        /** Move cursor to start of file */
        file_start(): void;
        /** Open Find dialog, optionally searching for text */
        find(text?: string): void;
        /** Select next Find result */
        find_next(): void;
        /** Select previous Find result */
        find_previous(): void;
        /** Remove a tab stop of indentation */
        indent_less(): void;
        /** Add a tab stop of indentation */
        indent_more(): void;
        /** Move cursor to line <n> */
        jump_line(n: number): void;
        /** Move cursor left one column */
        left(): void;
        /** Create a new line identical to the current line */
        line_clone(): void;
        /** Move cursor to end of line */
        line_end(): void;
        /** Insert line below cursor */
        line_insert_down(): void;
        /** Insert line above cursor */
        line_insert_up(): void;
        /** Move cursor to start of line */
        line_start(): void;
        /** Swap the current line with the line below */
        line_swap_down(): void;
        /** Swap the current line with the line above */
        line_swap_up(): void;
        /** Move cursor down one page */
        page_down(): void;
        /** Move cursor up one page */
        page_up(): void;
        /** Move cursor to the end of the current paragraph */
        paragraph_end(): void;
        /** Move cursor to the start of the current paragraph */
        paragraph_start(): void;
        /** Paste clipboard at cursor */
        paste(): void;
        /** Paste clipboard without style information */
        paste_match_style(): void;
        /** Redo */
        redo(): void;
        /** Move cursor right one column */
        right(): void;
        /** Save current document */
        save(): void;
        /** Select all text in the current document */
        select_all(): void;
        /** Select entire line <n>, or current line */
        select_line(n?: number): void;
        /** Select entire lines from <a> to <b> */
        select_lines(a: number, b: number): void;
        /** Clear current selection */
        select_none(): void;
        /** Select the entire nearest paragraph */
        select_paragraph(): void;
        /** Select word under cursor */
        select_word(): void;
        /** Get currently selected text */
        selected_text(): string;
        /** Insert a copy of the current selection */
        selection_clone(): void;
        /** Undo */
        undo(): void;
        /** Move cursor up one row */
        up(): void;
        /** Move cursor left one word */
        word_left(): void;
        /** Move cursor right one word */
        word_right(): void;
        /** Zoom in */
        zoom_in(): void;
        /** Zoom out */
        zoom_out(): void;
        /** Zoom to original size */
        zoom_reset(): void;
    };
    list: {
        /** Append to a list */
        append(l: any[], value: any): null;
        /** Clear a list */
        clear(l: any[]): null;
        /** Check if value appears in list */
        contains(l: any[], value: any): boolean;
        /** Copy a list */
        copy(l: any[]): any[];
        /** Count the number of times value appears in a list */
        count(l: any[], value: any): number;
        /** Append every item of b to a */
        extend(a: any[], b: any[]): null;
        /** Get list[index] */
        get(l: any[], index: number): any;
        /** Get the first index of value */
        index(l: any[], value: any): number;
        /** Insert value into list at index */
        insert(l: any[], index: number, value: any): number;
        /** Create an empty list */
        new(): any[];
        /** Remove and return item from list at index */
        pop(l: any[], index?: number): any;
        /** Remove value from list */
        remove(l: any[], value: any): null;
        /** Reverse list in place */
        reverse(l: any[]): null;
        /** Set list[index] = value */
        set(l: any[], index: number, value: any): null;
        /** Sort list in place */
        sort(l: any[]): null;
    };
    math: {
        /** Compute the absolute value of x */
        abs(x: number): number;
        /** Compute the arc cosine of x, in radians */
        acos(x: number): number;
        /** Compute the inverse hyperbolic cosine of x */
        acosh(x: number): number;
        /** Compute the arc sine of x, in radians */
        asin(x: number): number;
        /** Compute the inverse hyperbolic sine of x */
        asinh(x: number): number;
        /** Compute the arc tangent of x, in radians */
        atan(x: number): number;
        /** Compute the arc tangent of (x / y), in radians */
        atan2(x: number, y: number): number;
        /** Compute the inverse hyperbolic tangent of x */
        atanh(x: number): number;
        /** Convert number to binary string */
        bin(n: any): string;
        /** Compute the cube root of x */
        cbrt(x: number): number;
        /** Compute the smallest integer greater than or equal to x */
        ceil(x: number): number;
        /** Compute the number of ways to choose k from n unordered */
        comb(n: number, k: number): number;
        /** Compute the value of x with the sign of y */
        copysign(x: number, y: number): number;
        /** Compute the cosine of x, in radians */
        cos(x: number): number;
        /** Compute the hyperbolic cosine of x */
        cosh(x: number): number;
        /** Convert the angle x from radians to degrees */
        degrees(x: number): number;
        /** Get the constant e */
        e(): number;
        /** Compute the error function of x */
        erf(x: number): number;
        /** Compute the complimentary error function of x */
        erfc(x: number): number;
        /** Compute e ** x */
        exp(x: number): number;
        /** Compute 2 ** x */
        exp2(x: number): number;
        /** Compute e ** x - 1 */
        expm1(x: number): number;
        /** Compute the factorial of n */
        factorial(n: number): number;
        /** Compute the largest integer less than or equal to x */
        floor(x: number): number;
        /** Compute floating point modulo of x % y */
        fmod(x: number, y: number): number;
        /** Get the floating point exponent of x */
        frexp_e(x: number): number;
        /** Get the floating point mantissa of x */
        frexp_m(x: number): number;
        /** Compute the gamma function of x */
        gamma(x: number): number;
        /** Convert number to hex string */
        hex(n: any): string;
        /** Get the constant inf */
        inf(): number;
        /** Convert string to integer */
        int(s: string, base?: number): number;
        /** Check whether a is close to b */
        isclose(a: number, b: number): boolean;
        /** Check whether x is a finite number */
        isfinite(x: number): boolean;
        /** Check whether x is infinity */
        isinf(x: number): boolean;
        /** Check whether x is NaN */
        isnan(x: number): boolean;
        /** Compute integer square root of n */
        isqrt(n: number): number;
        /** Combine a mantissa and exponent into a float */
        ldexp(m: number, e: number): number;
        /** Compute the log gamma function of x */
        lgamma(x: number): number;
        /** Compute the natural log of x */
        log(x: number): number;
        /** Compute the natural log of 1+x */
        log1p(x: number): number;
        /** Compute the base-2 log of x */
        log2(x: number): number;
        /** Compute the base-n log of x */
        logn(x: number, n: number): number;
        /** Select the larger number */
        max(a: number, b: number): number;
        /** Select the smaller number */
        min(a: number, b: number): number;
        /** Compute modulo of x % y */
        mod(x: number, y: number): number;
        /** Get the fractional part of x */
        modf_f(x: number): number;
        /** Get the integer part of x */
        modf_i(x: number): number;
        /** Get the constant nan */
        nan(): number;
        /** Convert number to octal string */
        oct(n: any): string;
        /** Compute the ways to choose k items from n ordered */
        perm(n: number, k?: number | null): number;
        /** Get the constant pi */
        pi(): number;
        /** Compute x raised to the power y */
        pow(x: number, y: number): number;
        /** Convert the angle x from degrees to radians */
        radians(x: number): number;
        /** Generate random number between 0.0 - 1.0 */
        random(): number;
        /** Generate random number where a <= n < b */
        randrange(a: number, b: number): number;
        /** Compute the remainder of x / y */
        remainder(x: number, y: number): number;
        /** Round to nearest, with optional precision */
        round(n: number, precision?: number | null): number;
        /** Compute the sine of x, in radians */
        sin(x: number): number;
        /** Compute the hyperbolic sine of x */
        sinh(x: number): number;
        /** Compute the square root of x */
        sqrt(x: number): number;
        /** Compute the tangent of x, in radians */
        tan(x: number): number;
        /** Compute the hyperbolic tangent of x */
        tanh(x: number): number;
        /** Get the constant tau */
        tau(): number;
        /** Get the integer part of x */
        trunc(x: number): number;
        /** Generate n cryptographically random bytes */
        urandom(n: number): Uint8Array;
    };
    menu: {
        /** Check for updates */
        check_for_updates(): void;
        /** Open Debug window */
        open_debug_window(): void;
        /** Open Talon log */
        open_log(): void;
        /** Open Talon REPL */
        open_repl(): void;
        /** Open Talon config folder */
        open_talon_home(): void;
    };
    migrate: {
        /** Backup the .talon/user/ directory to a zip file in .talon/backups/ */
        backup_user(): void;
        /** Perform migrations for Talon v0.2 on all files in user/ */
        v02_all(prefix?: string, verbose?: boolean): void;
        /** Migrate action() definitions from a .talon file to a new Python file. */
        v02_one(path: string, verbose?: boolean): void;
    };
    mode: {
        /** Disable a mode */
        disable(mode: string): void;
        /** Enable a mode */
        enable(mode: string): void;
        /** Restore saved modes */
        restore(): void;
        /** Save all active modes */
        save(): void;
        /** Toggle a mode */
        toggle(mode: string): void;
    };
    path: {
        /** Path to Talon application */
        talon_app(): string;
        /** Path to home/.talon */
        talon_home(): string;
        /** Path to Talon user */
        talon_user(): string;
        /** Path to user home */
        user_home(): string;
    };
    set: {
        /** Add value to set */
        add(s: Set<any>, value: any): null;
        /** Clear set */
        clear(s: Set<any>): null;
        /** Check if value appears in set */
        contains(s: Set<any>, value: any): boolean;
        /** Copy set */
        copy(s: Set<any>): Set<any>;
        /** Get the difference of two sets */
        difference(a: Set<any>, b: Set<any>): Set<any>;
        /** Remove value from set if it exists */
        discard(s: Set<any>, value: any): null;
        /** Get the intersection of two sets */
        intersection(a: Set<any>, b: Set<any>): Set<any>;
        /** True if a and b don't intersect */
        isdisjoint(a: Set<any>, b: Set<any>): boolean;
        /** True if b contains a */
        issubset(a: Set<any>, b: Set<any>): boolean;
        /** True if a contains b */
        issuperset(a: Set<any>, b: Set<any>): boolean;
        /** Create an empty set */
        new(): Set<any>;
        /** Remove and return arbitrary set item */
        pop(s: Set<any>): any;
        /** Remove value from set */
        remove(s: Set<any>, value: any): null;
        /** Get all values present in exactly one of the provided sets */
        symmetric_difference(a: Set<any>, b: Set<any>): Set<any>;
        /** Get the union of a and b */
        union(a: Set<any>, b: Set<any>): Set<any>;
        /** Add all items from b to a */
        update(a: Set<any>, b: Set<any>): null;
    };
    sound: {
        /** Return active microphone name */
        active_microphone(): string;
        /** Return a list of available microphone names */
        microphones(): string[];
        /** Set the currently active microphone */
        set_microphone(name: string): void;
    };
    speech: {
        /** Disable speech recognition */
        disable(): void;
        /** Enable speech recognition */
        enable(): void;
        /** Test if speech recognition is enabled */
        enabled(): boolean;
        /** Record the phrase audio to a flac file */
        record_flac(): void;
        /** Record the phrase audio to a wave file */
        record_wav(): void;
        /** Replay a .flac or .wav file into the speech engine */
        replay(path: string): void;
        /** Set the currently active microphone - DEPRECATED: use sound.set_microphone() */
        set_microphone(name: string): void;
        /** Toggle speech recognition */
        toggle(value?: boolean): void;
    };
    string: {
        /** Capitalize the first letter of string */
        capitalize(s: string): string;
        /** Case fold string */
        casefold(s: string): string;
        /** Center string by padding to width */
        center(s: string, width: number, fillchar?: string | null): string;
        /** Convert a Unicode code point into a string */
        chr(i: number): string;
        /** Check whether haystack contains needle */
        contains(haystack: string, needle: string): boolean;
        /** Count the number of instances of sub in string, with optional start/end */
        count(s: string, sub: string, start?: number | null, end?: number | null): string;
        /** Encode string to bytes */
        encode(s: string, encoding?: string): Uint8Array;
        /** Check whether string ends with suffix */
        endswith(s: string, suffix: string): boolean;
        /** Expand tabs to spaces */
        expandtabs(s: string, tabsize?: number): string;
        /** Find sub in string, with optional start/end */
        find(s: string, sub: string, start?: number | null, end?: number | null): void;
        /** Find sub in string, with optional start/end, raising an error if not found */
        index(s: string, sub: string, start?: number | null, end?: number | null): void;
        /** Check if string contains only alphanumeric characters */
        isalnum(s: string): boolean;
        /** Check if string contains only alphabet characters */
        isalpha(s: string): boolean;
        /** Check if string contains only ascii characters */
        isascii(s: string): boolean;
        /** Check if string contains only decimal characters */
        isdecimal(s: string): boolean;
        /** Check if string contains only digits */
        isdigit(s: string): boolean;
        /** Check if string is lowercase */
        islower(s: string): boolean;
        /** Check if string contains only printable characters */
        isprintable(s: string): boolean;
        /** Check if string contains only whitespace characters */
        isspace(s: string): boolean;
        /** Check if string is title cased */
        istitle(s: string): boolean;
        /** Check if string is uppercase */
        isupper(s: string): boolean;
        /** Join a sequence using string */
        join(s: string, sequence: string[]): string;
        /** Left justify string by padding to width */
        ljust(s: string, width: number, fillchar?: string | null): string;
        /** Lowercase string */
        lower(s: string): string;
        /** Strip characters from the left of string */
        lstrip(s: string, chars?: string | null): string;
        /** Convert a character into a Unicode code point */
        ord(s: string): number;
        /** Remove prefix from string if present */
        removeprefix(s: string, prefix: string): string;
        /** Remove suffix from string if present */
        removesuffix(s: string, suffix: string): string;
        /** Replace [count] instances of old with new */
        replace(s: string, old: string, new_: string, count?: number): string;
        /** Find sub in string (from the right), with optional start/end */
        rfind(s: string, sub: string, start?: number | null, end?: number | null): void;
        /** Find sub in string (from the right), with optional start/end, raising an error if not found */
        rindex(s: string, sub: string, start?: number | null, end?: number | null): void;
        /** Right justify string by padding to width */
        rjust(s: string, width: number, fillchar?: string | null): string;
        /** Split using separator or whitespace [maxsplit] times from the right */
        rsplit(s: string, sep?: string | null, maxsplit?: number): string;
        /** Strip characters from the right of string */
        rstrip(s: string, chars?: string | null): string;
        /** Slice string, following python slicing rules [a:b:c] */
        slice(s: string, a: number, b?: number | null, c?: number | null): void;
        /** Split using separator or whitespace [maxsplit] times */
        split(s: string, sep?: string | null, maxsplit?: number): string;
        /** Split string into a list of lines */
        splitlines(s: string, keepends?: boolean): string[];
        /** Check whether string starts with prefix */
        startswith(s: string, prefix: string): boolean;
        /** Strip characters from both sides of string */
        strip(s: string, chars?: string | null): string;
        /** Swap the case of string */
        swapcase(s: string): string;
        /** Titlecase string */
        title(s: string): string;
        /** Uppercase string */
        upper(s: string): string;
    };
    time: {
        /** Get the day from a datetime */
        day(dt: Date): number;
        /** Format a datetime strftime-style */
        format(dt: Date, fmt: string): string;
        /** Get a datetime from ISO 8601 format */
        fromisoformat(s: string): Date;
        /** Get datetime from unix timestamp */
        fromtimestamp(ts: number): Date;
        /** Get datetime from UTC unix timestamp */
        fromutctimestamp(ts: number): Date;
        /** Get the hour from a datetime */
        hour(dt: Date): number;
        /** Format a datetime using ISO 8601 */
        isoformat(dt: Date): string;
        /** Get the microseconds from a datetime */
        microsecond(dt: Date): number;
        /** Get the minute from a datetime */
        minute(dt: Date): number;
        /** Get monotonic system time */
        monotonic(): number;
        /** Get the month from a datetime */
        month(dt: Date): number;
        /** Get the current date/time */
        now(): Date;
        /** Parse a datetime, strptime-style */
        parse(s: string, fmt: string): Date;
        /** Get the seconds from a datetime */
        second(dt: Date): number;
        /** Get unix timestamp from datetime */
        timestamp(dt: Date): number;
        /** Get the current date/time in UTC */
        utcnow(): Date;
        /** Get UTC unix timestamp from datetime */
        utctimestamp(dt: Date): number;
        /** Get the year from a datetime */
        year(dt: Date): number;
    };
    tracking: {
        /** Calibrate Eye Tracking */
        calibrate(): null;
        /** Is Control Mouse (Legacy) Enabled? */
        control1_enabled(): boolean;
        /** Toggle Control Mouse (Legacy) */
        control1_toggle(state?: boolean): null;
        /** Toggle Camera View */
        control_camera_toggle(state?: boolean): null;
        /** Toggle Control Mouse 2 (Debug View) */
        control_debug_toggle(state?: boolean): null;
        /** Is Control Mouse Enabled? */
        control_enabled(): boolean;
        /** Toggle Control Mouse 2 (Gaze Focus) */
        control_gaze_focus_toggle(state?: boolean): null;
        /** Toggle Control Mouse 2 (Gaze Control) */
        control_gaze_toggle(state?: boolean): null;
        /** Toggle Control Mouse 2 (Head Control) */
        control_head_toggle(state?: boolean): null;
        /** Toggle Control Mouse 2 (Mouse Jump) */
        control_mouse_jump_toggle(state?: boolean): null;
        /** Toggle Control Mouse */
        control_toggle(state?: boolean): null;
        /** Is Control Mouse (Zoom) Enabled? */
        control_zoom_enabled(): boolean;
        /** Toggle Control Mouse (Zoom) */
        control_zoom_toggle(state?: boolean): null;
        /** Trigger Eye Zoom / Click */
        zoom(): null;
        /** Cancel Eye Zoom */
        zoom_cancel(): null;
    };
    tuple: {
        /** Check if value appears in tuple */
        contains(t: any[], value: any): boolean;
        /** Count the number of times value appears in tuple */
        count(t: any[], value: any): number;
        /** Get the first index of value */
        index(t: any[], value: any): number;
        /** Create an empty tuple */
        new(): any[];
    };
    types: {
        /** Create a bytes object */
        bytes(v?: any): string;
        /** Create a dict */
        dict(): Record<string, any>;
        /** Create a list */
        list(v?: any): any;
        /** Get an instance of None */
        none(): null;
        /** Create a set */
        set(v?: any): Set<any>;
        /** Create a string */
        str(v?: any): string;
        /** Create a tuple */
        tuple(v?: any): any[];
    };
    win: {
        /** Return the open file's extension */
        file_ext(): string;
        /** Return the open filename */
        filename(): string;
        /** Get window title */
        title(): string;
    };
    user: {
        /** Abort current spoken phrase */
        abort_current_phrase(): void;
        /** Abort/cancel current spoken phrase */
        abort_phrase_command(): void;
        /** Abort the specified phrases */
        abort_specific_phrases(phrases: string[], start: number, end: number): void;
        /** Create dict */
        as_dict(arg1?: any, arg2?: any, arg3?: any, arg4?: any): Record<string, any>;
        /** Create list */
        as_list(arg1?: any, arg2?: any, arg3?: any, arg4?: any): any[];
        /** Assert that the values are equal */
        assert_equals(expected: any, found: any, message?: string): void;
        /** Focus browser and define phrase <text> */
        browser_define(text: string): void;
        /** Focus browser and define selected text */
        browser_define_selected(): void;
        /** Focus default browser */
        browser_focus_default(): void;
        /** Focus browser and open url */
        browser_open(url: string): void;
        /** Focus browser and search for <text> */
        browser_search(text: string): void;
        /** Focus browser and search for selected text */
        browser_search_selected(): void;
        /** Focus browser and translate <text> */
        browser_translate(text: string): void;
        /** Focus browser and translate selected text */
        browser_translate_selected(): void;
        /** Search for target text in browser */
        c_browser_search_target(target: any): void;
        /** Insert cursorless snippet <name> */
        c_insert_snippet(destination: any, name: string): void;
        /** Use developed folder of cursorless-talon */
        c_use_develop(): void;
        /** Use main branch of cursorless-talon */
        c_use_release(): void;
        /** Wrap the target with snippet <name> */
        c_wrap_with_snippet(target: any, name: string): void;
        /** Wrap the target with <symbol> */
        c_wrap_with_symbol(target: any, symbol: string): void;
        /** Change language mode */
        change_language(language?: string): void;
        /** Change sound device. */
        change_sound_device(name: string): void;
        /** Clear current line */
        clear_line(): void;
        /** Clear all current subtitles and notifications */
        clear_subtitles(): void;
        /** Set clipboard text without monitoring */
        clip_set_transient_text(text: string): void;
        /** Send command without targets to the clipboard manager */
        clippy_command_no_targets(command_id: string): void;
        /** Send a command with targets to the clipboard manager */
        clippy_command_with_targets(command_id: string, targets: any[]): void;
        /** Get clipboard targets */
        clippy_get(targets: any[]): void;
        /** Paste items from the clipboard manager at the given indices */
        clippy_paste_indices(indices: number[]): void;
        /** Rename clipboard targets to <text> */
        clippy_rename(targets: any[], text?: string | null): void;
        /** Search for <text> in the clipboard manager */
        clippy_search(text: string): void;
        /** Clears the forced language and re-enables code.language: extension matching */
        code_automatic_language(): void;
        /** Call function <name> */
        code_call_function(name: string): void;
        /** Declare class <name> */
        code_class(name: string, modifiers: string[]): void;
        /** Declare class <name> */
        code_class_wrapper(name: string, modifiers: string[] | string): void;
        /** Close last open tag */
        code_close_tag(): void;
        /** Constructor declaration */
        code_constructor(modifiers: string[]): void;
        /** Constructor declaration wrapper */
        code_constructor_wrapper(modifiers: string[] | string): void;
        /** Declare function <name> */
        code_function(name: string, modifiers: string[]): void;
        /** Main function declaration */
        code_function_main(): void;
        /** Declare function <name> */
        code_function_wrapper(name: string, modifiers: string[] | string): void;
        /** Get variable format */
        code_get_class_format(): string;
        /** Get class name */
        code_get_class_name(): string | null;
        /** Get function format */
        code_get_function_format(): string;
        /** Get class name */
        code_get_open_tag_name(): string | null;
        /** Get variable format */
        code_get_variable_format(): string;
        /** Insert attribute <name> */
        code_insert_attribute(name: string): void;
        /** Insert element <name> */
        code_insert_element(name: string): void;
        /** Insert return type <type> */
        code_insert_return_type(type: string): void;
        /** Insert type annotation <type> */
        code_insert_type_annotation(type: string): void;
        /** Insert link <text> */
        code_markdown_link(text?: string): void;
        /** Declare method <name> */
        code_method(name: string, modifiers: string[]): void;
        /** Declare method <name> */
        code_method_wrapper(name: string, modifiers: string[] | string): void;
        /** Create new instance of <name> */
        code_new_instance(name: string): void;
        /** Forces the active programming language to <language> and disables extension matching */
        code_set_language(language: string): void;
        /** Variable statement */
        code_variable(name: string, modifiers: string[], assign: boolean, data_type?: string): void;
        /** Variable statement wrapper */
        code_variable_wrapper(name: string, modifiers: string[] | string, assign: boolean, data_type?: string): void;
        /** Toggle between command and dictation mode */
        command_dictation_mode_toggle(): void;
        /** Clear the history */
        command_history_clear(): void;
        /** Toggles viewing the history */
        command_history_toggle(): void;
        /** Enter command mode and re-evaluate phrase */
        command_mode(phrase?: Phrase | string): void;
        /** The dirctory which contains the files required for communication between
        the application and Talon. This is the only function which absolutely
        must be implemented for any application using the command-client.  Each
        application that supports file-based RPC should use its own directory
        name.  Note that this action should only return a name; the parent
        directory is determined by the core command client code. */
        command_server_directory(): string;
        /** Copy all text in the current document */
        copy_all(): void;
        /** Copy the command id of the focused menu item */
        copy_command_id(): void;
        /** Copy current line */
        copy_line(): void;
        /** Copy end of current line */
        copy_line_end(): void;
        /** Copy start of current line */
        copy_line_start(): void;
        /** Copy paragraph under the cursor */
        copy_paragraph(): void;
        /** Copy word under cursor */
        copy_word(): void;
        /** Perform cursorless command on target */
        cursorless_command(action_name: string, target: any): void;
        /** Cursorless: Create destination from target */
        cursorless_create_destination(target: any, insertion_mode?: "to" | "before" | "after"): any;
        /** Cursorless: Run custom parsed command */
        cursorless_custom_command(content: string, arg1?: any | null, arg2?: any | null, arg3?: any | null): void;
        /** Get target text. If hide_decorations is True, don't show decorations */
        cursorless_get_text(target: any, hide_decorations?: boolean): string;
        /** Get texts for multiple targets. If hide_decorations is True, don't show decorations */
        cursorless_get_text_list(target: any, hide_decorations?: boolean): string[];
        /** Perform ide command on cursorless target */
        cursorless_ide_command(command_id: string, target: any): void;
        /** Perform text insertion on Cursorless destination */
        cursorless_insert(destination: any, text: string | string[]): void;
        /** Cursorless: Insert custom snippet <body> */
        cursorless_insert_snippet(body: string, destination?: any, scope_type?: string | string[] | null): void;
        /** Cursorless: Insert named snippet <name> */
        cursorless_insert_snippet_by_name(name: string): void;
        /** Cursorless private api: Highlights a target */
        cursorless_private_action_highlight(target: any, highlightId?: string | null): null;
        /** Cursorless private api low-level target builder: Create a list target */
        cursorless_private_build_list_target(elements: any[]): any;
        /** Cursorless private api low-level target builder: Create a primitive target */
        cursorless_private_build_primitive_target(modifiers: Record<string, any>[], mark: Record<string, any> | null): any;
        /** Cursorless private api: Extract all decorated marks from a Talon capture */
        cursorless_private_extract_decorated_marks(capture: any): Record<string, any>[];
        /** Cursorless private api: Creates the "nothing" target */
        cursorless_private_target_nothing(): any;
        /** Start recording Cursorless tests, without confirmation popup windows */
        cursorless_record_silent_test(): void;
        /** Execute Cursorless reformat action. Reformat target with formatter */
        cursorless_reformat(target: any, formatters: string): void;
        /** Perform vscode command on cursorless target

        Deprecated: prefer `cursorless_ide_command` */
        cursorless_vscode_command(command_id: string, target: any): void;
        /** Cursorless: Wrap target with custom snippet <body> */
        cursorless_wrap_with_snippet(body: string, target: any, variable_name?: string | null, scope?: string | null): void;
        /** Cursorless: Wrap target with a named snippet <name> */
        cursorless_wrap_with_snippet_by_name(name: string, variable_name: string, target: any): void;
        /** Cut all text in the current document */
        cut_all(): void;
        /** Cut current line */
        cut_line(): void;
        /** Cut end of current line */
        cut_line_end(): void;
        /** Cut start of current line */
        cut_line_start(): void;
        /** Cut paragraph under the cursor */
        cut_paragraph(): void;
        /** Cut word under cursor */
        cut_word(): void;
        /** Return string with todays date */
        date_today(): string;
        /** Return string with tomorrow date */
        date_tomorrow(): string;
        /** Return string with yesterdays date */
        date_yesterday(): string;
        /** Replacing camelCase boundaries with blank space */
        de_camel(text: string): string;
        /** Log debug message */
        debug(message: string): void;
        /** Delete end of current line */
        delete_line_end(): void;
        /** Delete start of current line */
        delete_line_start(): void;
        /** Delete character to the right */
        delete_right(): void;
        /** Delete word to the left */
        delete_word_left(): void;
        /** Delete word to the right */
        delete_word_right(): void;
        /** Insert delimiter pair <left> and <right> with interior <middle> */
        delimiters_pair_insert(left: string, right: string, middle?: string): void;
        /** Insert matching delimiters pair <pair_name> */
        delimiters_pair_insert_by_name(pair_name: string): void;
        /** Wrap selection with matching delimiter pair <pair_name> */
        delimiters_pair_wrap_selection(pair_name: string): void;
        /** Wrap selection with delimiters <left> and <right> */
        delimiters_pair_wrap_selection_with(left: string, right: string): void;
        /** Enter demo mode */
        demo_mode(): void;
        /** Resets the dictation formatter */
        dictation_format_reset(): void;
        /** Returns the text before and after the current selection */
        dictation_get_context(): [string | null, string | null];
        /** Inserts dictated text, formatted appropriately. */
        dictation_insert(text: string): void;
        /** Enter dictation mode and re-evaluate phrase */
        dictation_mode(phrase?: Phrase | string): void;
        /** Returns true if a `,` should be inserted between these words during dictation */
        dictation_needs_comma_between(before: string, after: string): boolean;
        /** Indicates whether the pre-phrase signal was emitted at the start of this phrase */
        did_emit_pre_phrase_signal(): boolean;
        /** Returns the current mute status */
        discord_get_mute_status(): boolean;
        /** Gets the selected discord voice channel */
        discord_get_selected_voice_channel(): Record<string, any> | null;
        /** Sets the Discord mute status */
        discord_set_mute_status(mute: boolean): boolean;
        /** Toggles the mute status on Discord */
        discord_toggle_mute(): boolean;
        /** Returns the current Discord voice settings */
        discord_voice_settings(): Record<string, any>;
        /** Discard draft editor */
        draft_editor_discard(): void;
        /** Open draft editor */
        draft_editor_open(): void;
        /** Paste last submitted draft */
        draft_editor_paste_last(): void;
        /** Submit/save draft editor */
        draft_editor_submit(): void;
        /** Perform edit command */
        edit_command(action: any, modifiers: any[]): void;
        /** Perform edit bring command */
        edit_command_bring(source: any[], destination: any[]): void;
        /** Copy selection to clipboard */
        edit_copy(): void;
        /** Cut selection to clipboard */
        edit_cut(): void;
        /** Paste clipboard at cursor */
        edit_paste(expand: boolean): void;
        /** Test edit.paste() */
        edit_test_paste(): void;
        /** Test user.paste_text() */
        edit_test_paste_text(): void;
        /** Edit vocabulary Talon list */
        edit_vocabulary(): void;
        /** Edit words to replace csv */
        edit_words_to_replace(): void;
        /** If in an application supporting the command client, returns True
        and touches a file to indicate that a phrase is beginning execution.
        Otherwise does nothing and returns False. */
        emit_pre_phrase_signal(): boolean;
        /** Execute command */
        exec(command: string): void;
        /** Open file manager at the given path */
        file_manager_open(path: string): void;
        /** Find in entire project/all files */
        find_everywhere(text?: string): void;
        /** Find file <text> */
        find_file(text?: string): void;
        /** Find and replace in current file/editor */
        find_replace(text?: string): void;
        /** Confirm replace current */
        find_replace_confirm(): void;
        /** Confirm replace all */
        find_replace_confirm_all(): void;
        /** Find and replace in entire project/all files */
        find_replace_everywhere(text?: string): void;
        /** Toggles replace preserve case */
        find_replace_toggle_preserve_case(): void;
        /** Find sibling file based on file name */
        find_sibling_file(): void;
        /** Toggles find match by case sensitivity */
        find_toggle_match_by_case(): void;
        /** Toggles find match by regex */
        find_toggle_match_by_regex(): void;
        /** Toggles find match by whole words */
        find_toggle_match_by_word(): void;
        /** Focus app and wait until finished */
        focus_app(app: App): void;
        /** Focus desktop */
        focus_desktop(): void;
        /** Focus application number <number> */
        focus_number(number: number): void;
        /** Focus window and wait until finished */
        focus_window(window: Window): void;
        /** Foot switch button center:down */
        foot_switch_center_down(): void;
        /** Foot switch button center:up */
        foot_switch_center_up(held: boolean): void;
        /** Foot switch key down event. Left(0), Center(1), Right(2), Top(3) */
        foot_switch_down_event(key: number): void;
        /** Foot switch button left:down */
        foot_switch_left_down(): void;
        /** Foot switch button left:up */
        foot_switch_left_up(held: boolean): void;
        /** Foot switch button right:down */
        foot_switch_right_down(): void;
        /** Foot switch button right:up */
        foot_switch_right_up(held: boolean): void;
        /** Reverse scroll direction using foot switch */
        foot_switch_scroll_reverse(): void;
        /** Foot switch button top:down */
        foot_switch_top_down(): void;
        /** Foot switch button top:up */
        foot_switch_top_up(held: boolean): void;
        /** Foot switch key up event. Left(0), Center(1), Right(2), Top(3) */
        foot_switch_up_event(key: number): void;
        /** Format document */
        format_document(): void;
        /** Formats <text> as <formatters> */
        format_text(text: string, formatters: string): string;
        /** Disable game mode */
        game_mode_disable(): void;
        /** Enable game mode */
        game_mode_enable(): void;
        /** Toggle voice chat for game */
        game_toggle_mute(): void;
        /** Gamepad press button <button> */
        gamepad_button_down(button: string): void;
        /** Gamepad release button <button> */
        gamepad_button_up(button: string): void;
        /** Gamepad press button dpad down */
        gamepad_press_dpad_down(): void;
        /** Gamepad press button dpad left */
        gamepad_press_dpad_left(): void;
        /** Gamepad press button dpad right */
        gamepad_press_dpad_right(): void;
        /** Gamepad press button dpad up */
        gamepad_press_dpad_up(): void;
        /** Gamepad press button east */
        gamepad_press_east(): void;
        /** Gamepad press button left shoulder */
        gamepad_press_left_shoulder(): void;
        /** Gamepad press button left thumb stick */
        gamepad_press_left_stick(): void;
        /** Gamepad press button north */
        gamepad_press_north(): void;
        /** Gamepad press button right shoulder */
        gamepad_press_right_shoulder(): void;
        /** Gamepad press button right thumb stick */
        gamepad_press_right_stick(): void;
        /** Gamepad press button select */
        gamepad_press_select(): void;
        /** Gamepad press button south */
        gamepad_press_south(): void;
        /** Gamepad press button start */
        gamepad_press_start(): void;
        /** Gamepad press button west */
        gamepad_press_west(): void;
        /** Gamepad release button dpad down */
        gamepad_release_dpad_down(held: boolean): void;
        /** Gamepad release button dpad left */
        gamepad_release_dpad_left(held: boolean): void;
        /** Gamepad release button dpad right */
        gamepad_release_dpad_right(held: boolean): void;
        /** Gamepad release button dpad up */
        gamepad_release_dpad_up(held: boolean): void;
        /** Gamepad release button east */
        gamepad_release_east(held: boolean): void;
        /** Gamepad release button left shoulder */
        gamepad_release_left_shoulder(held: boolean): void;
        /** Gamepad release button left thumb stick */
        gamepad_release_left_stick(held: boolean): void;
        /** Gamepad release button north */
        gamepad_release_north(held: boolean): void;
        /** Gamepad release button right shoulder */
        gamepad_release_right_shoulder(held: boolean): void;
        /** Gamepad release button right thumb stick */
        gamepad_release_right_stick(held: boolean): void;
        /** Gamepad release button select */
        gamepad_release_select(held: boolean): void;
        /** Gamepad release button south */
        gamepad_release_south(held: boolean): void;
        /** Gamepad release button start */
        gamepad_release_start(held: boolean): void;
        /** Gamepad release button west */
        gamepad_release_west(held: boolean): void;
        /** Gamepad left stick movement */
        gamepad_stick_left(x: number, y: number): void;
        /** Gamepad right stick movement */
        gamepad_stick_right(x: number, y: number): void;
        /** Indicates that a gamepad button has changed state */
        gamepad_tester_button(id: string, is_pressed: boolean): void;
        /** Indicates that a gamepad stick has changed state */
        gamepad_tester_stick(id: string, x: number, y: number): void;
        /** Toggle visibility of gamepad tester gui */
        gamepad_tester_toggle(): void;
        /** Indicates that a gamepad trigger has changed state */
        gamepad_tester_trigger(id: string, value: number): void;
        /** Gamepad trigger left movement */
        gamepad_trigger_left(value: number): void;
        /** Gamepad trigger right movement */
        gamepad_trigger_right(value: number): void;
        /** Get application by name */
        get_app(name: string): App;
        /** Get top window by application name */
        get_app_window(app_name: string): Window;
        /** Get matching sibling for extension */
        get_extension_sibling(extension: string): string;
        /** Get insertion snippet named <name> */
        get_insertion_snippet(name: string): any;
        /** Fetch a dict of running applications */
        get_running_applications(): Record<string, string>;
        /** Get snippet named <name> */
        get_snippet(name: string): any;
        /** Get the window under the mouse cursor */
        get_window_under_cursor(): Window;
        /** Get wrapper snippet named <name> */
        get_wrapper_snippet(name: string): any;
        /** Checkout branch <branch> */
        git_checkout(branch?: string | null, submit?: boolean): void;
        /** Cherry pick commit */
        git_cherry_pick(): void;
        /** Clone git repository */
        git_clone(): void;
        /** Commit changes <message> */
        git_commit(message?: string | null): void;
        /** Commit changes <message> */
        git_commit_amend(message?: string | null): void;
        /** Commit empty */
        git_commit_empty(): void;
        /** Copy remote git file URL to clipboard as markdown link */
        git_copy_markdown_remote_file_url(targets: any[]): void;
        /** Copy remote git file URL to clipboard */
        git_copy_remote_file_url(use_selection: boolean, use_branch: boolean): void;
        /** Create branch <branch> */
        git_create_branch(branch?: string | null): void;
        /** Create tag <tag> */
        git_create_tag(tag?: string | null): void;
        /** Create tag from clipboard */
        git_create_tag_clipboard(): void;
        /** Delete branch <branch> */
        git_delete_branch(branch?: string | null): void;
        /** Show git diff */
        git_diff(): void;
        /** Show git log */
        git_log(): void;
        /** Merge branch <branch> */
        git_merge(branch?: string | null): void;
        /** Show git statistics */
        git_numstat(since?: string | null): void;
        /** Open remote git file in browser */
        git_open_remote_file_url(use_selection: boolean, use_branch: boolean): void;
        /** Open remote repository in browser */
        git_open_url(command: string): void;
        /** Pull from remote */
        git_pull(): void;
        /** Push to remote */
        git_push(): void;
        /** Push tags to remote */
        git_push_tags(): void;
        /** Show git remote */
        git_remote(): void;
        /** Show branches */
        git_show_branches(): void;
        /** Show tags */
        git_show_tags(): void;
        /** Stage all files */
        git_stage_all(): void;
        /** Stash changes */
        git_stash(): void;
        /** List git stashes */
        git_stash_list(): void;
        /** Pop stash */
        git_stash_pop(): void;
        /** Show git stashes */
        git_stash_show(): void;
        /** Show git status */
        git_status(): void;
        /** Unstage all files */
        git_unstage_all(): void;
        /** Navigate back */
        go_back(): void;
        /** Navigate forward */
        go_forward(): void;
        /** Display contextual command info */
        help_active_toggle(): void;
        /** Toggle alphabet help gui */
        help_alphabet_toggle(): void;
        /** Display command info for specified context */
        help_context(m: string): void;
        /** Copy all commands to clipboard */
        help_copy_all_commands(): void;
        /** Toggle formatters help gui */
        help_formatters_toggle(): void;
        /** Hides the help */
        help_hide(): void;
        /** Toggle help key debug gui */
        help_key_debug_toggle(): void;
        /** Navigates to next page */
        help_next(): void;
        /** Navigates to previous page */
        help_previous(): void;
        /** Refreshes the help */
        help_refresh(): void;
        /** Returns to the main help window */
        help_return(): void;
        /** Hide running applications help gui */
        help_running_apps_hide(): void;
        /** Toggle running applications help gui */
        help_running_apps_toggle(): void;
        /** Toggle help scope gui */
        help_scope_toggle(): void;
        /** Display command info for search phrase */
        help_search(phrase: string): void;
        /** Show help search gui with actions results */
        help_search_actions(text: string): void;
        /** Show help search gui with command results */
        help_search_commands(text: string): void;
        /** Hide help search gui */
        help_search_hide(): void;
        /** Select context number <number> */
        help_select_number(number: number): void;
        /** Cycle homophones if the selected word is a homophone */
        homophones_cycle_selected(): void;
        /** Get homophones for the given word. Used by the phones action in cursorless */
        homophones_get(word: string): string[];
        /** Replace words with recently chosen homophones */
        homophones_replace_words(words: string[]): string[];
        /** Log info message */
        info(message: string): void;
        /** Insert arrow symbol */
        insert_arrow(): void;
        /** Insert clipboard content by key presses */
        insert_clipboard_with_keys(): void;
        /** Insert text <text> formatted as <formatters> */
        insert_formatted(text: string, formatters: string): void;
        /** Insert snippet */
        insert_snippet(body: string): void;
        /** Insert snippet <name> */
        insert_snippet_by_name(name: string, substitutions?: Record<string, string>): void;
        /** Insert snippet <name> with phrase <phrase> */
        insert_snippet_by_name_with_phrase(name: string, phrase: string): void;
        /** Add <symbol> at end of line and then insert line below */
        insert_symbol_and_break_at_end(symbol: string): void;
        /** Inserts a TODO comment snippet */
        insert_todo_comment_snippet(message?: string | null): void;
        /** Insert <text> with padding */
        insert_with_padding(text: string): void;
        /** Insert arrow function */
        js_arrow_function(name: string): void;
        /** Arrowify line */
        js_arrowify_line(): void;
        /** Simulate holding a key with repeated key presses */
        key_hold(key: string): void;
        /** Stop repeating key */
        key_release(key: string): void;
        /** Create a new line identical to the current line above the current line */
        line_clone_up(): void;
        /** Insert two lines below cursor */
        line_insert_down_twice(): void;
        /** Move cursor to middle of line */
        line_middle(): void;
        /** Inserts a lorem ipsum with <num_words> words */
        lorem_ipsum(num_words: number): void;
        /** Enter mixed mode and re-evaluate phrase */
        mixed_mode(phrase?: Phrase | string): void;
        /** Click mouse button */
        mouse_click(action: string): void;
        /** Click left mouse button. If scrolling or dragging, stop instead. */
        mouse_click_with_conditions(): void;
        /** Toggle enable/disable for the eye tracker */
        mouse_control_toggle(enable?: boolean | null): void;
        /** Toggle freeze cursor position updates for the eye tracker */
        mouse_freeze_toggle(): void;
        /** Starts gaze scroll */
        mouse_gaze_scroll(): void;
        /** Hides the cursor */
        mouse_hide_cursor(): void;
        /** Move the mouse cursor to the center of the active window */
        mouse_move_center_window(): void;
        /** Mouse on pop handler */
        mouse_on_pop(): void;
        /** Release held mouse buttons */
        mouse_release_held_buttons(): boolean;
        /** Scrolls */
        mouse_scroll(direction: string, times: number): void;
        /** Decrease scroll speed */
        mouse_scroll_speed_decrease(): void;
        /** Increase scroll speed */
        mouse_scroll_speed_increase(): void;
        /** Notify scroll speed */
        mouse_scroll_speed_notify(): void;
        /** Set scroll speed */
        mouse_scroll_speed_set(speed: number): void;
        /** Stop mouse scroll */
        mouse_scroll_stop(): void;
        /** Toggle scrolling continuously */
        mouse_scrolling(direction: string): void;
        /** Shows the cursor */
        mouse_show_cursor(): void;
        /** Disables control mouse and scroll */
        mouse_sleep(): void;
        /** Set control mouse to earlier state */
        mouse_wake(): void;
        /** Move active windows closest side to cursor position */
        move_window_side_to_cursor_position(): void;
        /** Move the active window to the center of the current screen */
        move_window_to_screen_center(): void;
        /** Noise cluck */
        noise_cluck(): void;
        /** Start or stop continuous noise using debounce */
        noise_debounce(name: string, active: boolean): void;
        /** Noise hiss started */
        noise_hiss_start(): void;
        /** Noise hiss stopped */
        noise_hiss_stop(): void;
        /** Noise pop */
        noise_pop(): void;
        /** Noise shush started */
        noise_shush_start(): void;
        /** Noise shush stopped */
        noise_shush_stop(): void;
        /** Show notification */
        notify(text: string): void;
        /** Create a new paragraph identical to the current paragraph below the current paragraph */
        paragraph_clone_down(): void;
        /** Create a new paragraph identical to the current paragraph above the current paragraph */
        paragraph_clone_up(): void;
        /** Insert paragraph below current paragraph */
        paragraph_insert_down(): void;
        /** Insert paragraph above current paragraph */
        paragraph_insert_up(): void;
        /** Paste to the current document */
        paste_all(): void;
        /** Paste to current line */
        paste_line(): void;
        /** Paste to end of current line */
        paste_line_end(): void;
        /** Paste to start of current line */
        paste_line_start(): void;
        /** Paste to paragraph under the cursor */
        paste_paragraph(): void;
        /** Pastes <text> and preserves clipboard */
        paste_text(text: string): void;
        /** Paste to word under cursor */
        paste_word(): void;
        /** Pick list item number <number> */
        pick_item(number: number): void;
        /** Perform cursorless action or ide command on target (internal use only) */
        private_cursorless_action_or_ide_command(instruction: Record<string, string>, target: any): void;
        /** Execute Cursorless move/bring action */
        private_cursorless_bring_move(action_name: string, targets: any): void;
        /** Execute Cursorless call action */
        private_cursorless_call(callee: any, argument?: any): void;
        /** Show new cursorless html cheat sheet */
        private_cursorless_cheat_sheet_show_html(): void;
        /** Update default cursorless cheatsheet json (for developer use only) */
        private_cursorless_cheat_sheet_update_json(): void;
        /** Execute cursorless command and wait for it to finish */
        private_cursorless_command_and_wait(action: Record<string, any>): void;
        /** Execute cursorless command and return result */
        private_cursorless_command_get(action: Record<string, any>): void;
        /** Execute cursorless command without waiting */
        private_cursorless_command_no_wait(action: Record<string, any>): void;
        /** Hides scope visualizer */
        private_cursorless_hide_scope_visualizer(): void;
        /** Cursorless: Insert community snippet <name> */
        private_cursorless_insert_community_snippet(name: string, destination: any): void;
        /** Execute Cursorless insert snippet action */
        private_cursorless_insert_snippet(insertion_snippet: any): void;
        /** Cursorless: Insert snippet <snippet_description> with phrase <text> */
        private_cursorless_insert_snippet_with_phrase(snippet_description: string, text: string): void;
        /** Test generating a snippet */
        private_cursorless_make_snippet_test(target: any): void;
        /** Open web page with cursorless instructions */
        private_cursorless_open_instructions(): void;
        /** Execute Cursorless paste action */
        private_cursorless_paste(destination: any): void;
        /** Start recording Cursorless error tests */
        private_cursorless_record_error_test(): void;
        /** Start recording Cursorless decoration tests */
        private_cursorless_record_highlights_test(): void;
        /** Start / stop recording Cursorless navigation tests */
        private_cursorless_record_navigation_test(): void;
        /** Start recording Cursorless that mark tests */
        private_cursorless_record_that_mark_test(): void;
        /** Execute command via rpc and wait for command to finish. */
        private_cursorless_run_rpc_command_and_wait(command_id: string, arg1?: any, arg2?: any): void;
        /** Execute command via rpc and return command output. */
        private_cursorless_run_rpc_command_get(command_id: string, arg1?: any, arg2?: any): any;
        /** Execute command via rpc and DON'T wait. */
        private_cursorless_run_rpc_command_no_wait(command_id: string, arg1?: any, arg2?: any): void;
        /** Show Cursorless command statistics */
        private_cursorless_show_command_statistics(): void;
        /** Shows scope visualizer */
        private_cursorless_show_scope_visualizer(scope_type: Record<string, any>, visualization_type: string): void;
        /** Show Cursorless-specific settings in ide */
        private_cursorless_show_settings_in_ide(): void;
        /** Show Cursorless-specific settings in ide */
        private_cursorless_show_sidebar(): void;
        /** Run Cursorless spoken form test */
        private_cursorless_spoken_form_test(phrase: string, mockedGetValue_: string | null): void;
        /** Enable/disable Cursorless spoken form test mode */
        private_cursorless_spoken_form_test_mode(enable: boolean): void;
        /** Execute Cursorless swap action */
        private_cursorless_swap(targets: any): void;
        /** Run test for Cursorless private highlight nothing api */
        private_cursorless_test_alternate_highlight_nothing(): void;
        /** Run test for Cursorless private extract decorated marks api */
        private_cursorless_test_extract_decorated_marks(target: any): void;
        /** Enable/disable cursorless community snippets in test mode */
        private_cursorless_use_community_snippets(enable: boolean): void;
        /** Cursorless: Wrap target with community snippet <name> */
        private_cursorless_wrap_with_community_snippet(name: string, target: any): void;
        /** Execute Cursorless wrap/rewrap with paired delimiter action */
        private_cursorless_wrap_with_paired_delimiter(action_name: string, target: any, paired_delimiter: string[]): void;
        /** Execute Cursorless wrap with snippet action */
        private_cursorless_wrap_with_snippet(action_name: string, target: any, snippet_location: string): void;
        /** Show quick pick */
        quick_pick_show(): void;
        /** Start recording */
        recording_start(): void;
        /** Stop recording */
        recording_stop(): void;
        /** Reformats the current selection as <formatters> */
        reformat_selection(formatters: string): void;
        /** Re-formats <text> as <formatters> */
        reformat_text(text: string, formatters: string): string;
        /** Re-evaluate and run phrase */
        rephrase(phrase: Phrase, run_async?: boolean): void;
        /** Resize active windows closest side to cursor position */
        resize_window_side_to_cursor_position(): void;
        /** Revert active window to last position */
        revert_active_window_position(): void;
        /** Revert window for application <app_name> to last position */
        revert_application_window_position(app_name: string): void;
        /** Revert the window under the cursor to last position */
        revert_window_under_cursor_position(): void;
        /** Execute command via RPC. */
        run_rpc_command(command_id: string, arg1?: any, arg2?: any, arg3?: any, arg4?: any, arg5?: any): void;
        /** Execute command via application command server and wait for command to finish. */
        run_rpc_command_and_wait(command_id: string, arg1?: any, arg2?: any, arg3?: any, arg4?: any, arg5?: any): void;
        /** Execute command via application command server and return command output. */
        run_rpc_command_get(command_id: string, arg1?: any, arg2?: any, arg3?: any, arg4?: any, arg5?: any): any;
        /** Save current document without formatting */
        save_without_formatting(): void;
        /** Get screen by number */
        screen_get_by_number(screen_number: number): Screen;
        /** Get screen by offset */
        screen_get_by_offset(offset: number): void;
        /** Show screen number on each screen */
        screens_show_numbering(): void;
        /** Takes a screenshot of the entire screen and saves it to the pictures folder.
        Optional screen number can be given to use screen other than main. */
        screenshot(screen_number?: number): void;
        /** Takes a screenshot of the entire screen and saves it to the clipboard.
        Optional screen number can be given to use screen other than main. */
        screenshot_clipboard(screen_number?: number): void;
        /** Triggers an application is capable of taking a screenshot of a portion of the screen */
        screenshot_selection(): void;
        /** Takes a screenshot of the active window and saves it to the pictures folder */
        screenshot_window(): void;
        /** Takes a screenshot of the active window and saves it to the clipboard */
        screenshot_window_clipboard(): void;
        /** Scroll down */
        scroll_down(): void;
        /** Scroll down continuously */
        scroll_down_continuous(): void;
        /** Scroll down half page */
        scroll_down_half_page(): void;
        /** Scroll down page */
        scroll_down_page(): void;
        /** Set scroll speed */
        scroll_speed(speed: number): void;
        /** Decrease scroll speed */
        scroll_speed_decrease(): void;
        /** Increase scroll speed */
        scroll_speed_increase(): void;
        /** Show scroll speed */
        scroll_speed_show(): void;
        /** Stop continuous scroll */
        scroll_stop(): void;
        /** Scroll up */
        scroll_up(): void;
        /** Scroll up continuously */
        scroll_up_continuous(): void;
        /** Scroll up half page */
        scroll_up_half_page(): void;
        /** Scroll up page */
        scroll_up_page(): void;
        /** Move selection down */
        select_down(): void;
        /** Select end of current line */
        select_line_end(): void;
        /** Select start of current line */
        select_line_start(): void;
        /** Selects the surrounding pair. */
        select_surrounding_pair(delimiter_name?: string): void;
        /** Selects the interior of a surrounding pair. */
        select_surrounding_pair_interior(delimiter_name?: string): void;
        /** Toggle selection */
        select_toggle(): void;
        /** Move selection up */
        select_up(): void;
        /** Select word to the left */
        select_word_left(): void;
        /** Select word to the right */
        select_word_right(): void;
        /** Insert a copy of the current selection before the selection */
        selection_clone_before(): void;
        /** Send key <key> to application */
        send_key(key: string, app: App): void;
        /** Opens the given search result on slack */
        slack_open_search_result(search: string): void;
        /** Move the active window to position <pos_name> on the current screen */
        snap_active_window_to_position(pos_name: string): void;
        /** Move the active window to screen <screen_desc> while retaining the same relative position */
        snap_active_window_to_screen(screen_desc: number | string): void;
        /** Move the active window to position <pos_name> on screen <screen_desc> */
        snap_active_window_to_screen_and_position(screen_desc: number | string, pos_name: string): void;
        /** Move window for application <app_name> to position <pos_name> on the current screen */
        snap_application_to_position(app_name: string, pos_name: string): void;
        /** Move window for application <app_name> to screen <screen_desc> while retaining the same relative position */
        snap_application_to_screen(app_name: string, screen_desc: number | string): void;
        /** Move window for application <app_name> to position <pos_name> on screen <screen_desc> */
        snap_application_to_screen_and_position(app_name: string, screen_desc: number | string, pos_name: string): void;
        /** Applies snap position <pos_name> to given rectangle */
        snap_apply_position_to_rect(rect: Rect, pos_name: string): Rect;
        /** Move the window under the cursor to position <pos_name> on the current screen */
        snap_window_under_cursor_to_position(pos_name: string): void;
        /** Move the window under the cursor to screen <screen_desc> while retaining the same relative position */
        snap_window_under_cursor_to_screen(screen_desc: number | string): void;
        /** Move the window under the cursor to position <pos_name> on screen <screen_desc> */
        snap_window_under_cursor_to_screen_and_position(screen_desc: number | string, pos_name: string): void;
        /** Enables or disables the microphone */
        sound_microphone_enable(enable: boolean): void;
        /** Event that triggers when the microphone is enabled or disabled */
        sound_microphone_enable_event(): void;
        /** Returns true if the microphone is NOT set to 'None' */
        sound_microphone_enabled(): boolean;
        /** Toggle the microphone */
        sound_microphone_toggle(): void;
        /** Stop current app actions */
        stop_app(): void;
        /** Swap active window position with application <app_name> */
        swap_active_window_position_with_application(app_name: string): void;
        /** Enter swedish dictation mode and re-evaluate phrase */
        swedish_dictation_mode(phrase?: Phrase | string): void;
        /** Hibernate operating system */
        system_hibernate(): void;
        /** Lock operating system */
        system_lock(): void;
        /** Restart operating system */
        system_restart(): void;
        /** Shutdown operating system */
        system_shutdown(): void;
        /** Jump to last used tab */
        tab_back(): void;
        /** Jumps to the final tab */
        tab_final(): void;
        /** Jumps to the specified tab */
        tab_jump(number: number): void;
        /** Jumps to the specified tab counted from the back */
        tab_jump_from_back(number: number): void;
        /** Move tab to the left */
        tab_move_left(): void;
        /** Move tab to the right */
        tab_move_right(): void;
        /** Adds os-specific context info to the clipboard for the focused app for .talon files */
        talon_add_context_clipboard(): void;
        /** Adds os-specific context info to the clipboard for the focused app for .py files. Assumes you've a Module named mod declared. */
        talon_add_context_clipboard_python(): void;
        /** Get path to talon application */
        talon_app(): string;
        /** Create a new python context file for the current application */
        talon_create_app_context(): void;
        /** Return buttons for Talon Deck */
        talon_deck_get_buttons(): Record<string, any>[];
        /** Update Talon Deck. This will trigger a call to `talon_deck_get_buttons()` */
        talon_deck_update(): void;
        /** Get actions list as text */
        talon_get_actions(): string;
        /** Get long actions list as text */
        talon_get_actions_long(): string;
        /** Get list of actions from search parameter */
        talon_get_actions_search(text: string): string;
        /** Get captures as text */
        talon_get_captures(): string;
        /** Get core lists and captures as text */
        talon_get_core(): string;
        /** Get lists as text */
        talon_get_lists(): string;
        /** Get modes as text */
        talon_get_modes(): string;
        /** Get tags as text */
        talon_get_tags(): string;
        /** Get path to talon home */
        talon_home(): string;
        /** Search for non alpha keys in meta lists */
        talon_print_list_problems(): void;
        /** Quit and relaunch the Talon app */
        talon_restart(): void;
        /** Sims the phrase in the active app and dumps to the log */
        talon_sim_phrase(phrase: string | Phrase): void;
        /** Put Talon to sleep */
        talon_sleep(): void;
        /** Get path to talon user */
        talon_user(): string;
        /** Wake Talon from sleep */
        talon_wake(): void;
        /** Returns true if Talon was just restarted */
        talon_was_restarted(): boolean;
        /** Start a new test suite */
        test_run_suite(suite_name: string, fixtures: any[], callback: () => void): void;
        /** Insert link <text> */
        testing(a: string, text?: string, number?: number): void;
        /** Toggle subtitles */
        toggle_subtitles(): void;
        /** Translate english text to swedish */
        translate_english_to_swedish(english_text: string): string;
        /** Issue keystroke to trigger command server to execute command that
        was written to the file.  For internal use only */
        trigger_command_server_command_execution(): void;
        /** Update given path */
        update_path(path: string): void;
        /** Get path to user home */
        user_home(): string;
        /** Volume decrease */
        volume_down(): void;
        /** Volume increase */
        volume_up(): void;
        /** Execute vscode command <command_id> */
        vscode(command_id: string, arg1?: any, arg2?: any, arg3?: any, arg4?: any, arg5?: any): void;
        /** Add all missing imports */
        vscode_add_missing_imports(): void;
        /** Execute command via vscode command server, if available, and wait
        for command to finish.  If command server not available, uses command
        palette and doesn't guarantee that it will wait for command to
        finish. */
        vscode_and_wait(command_id: string): void;
        /** Find recent session, directory or file */
        vscode_find_recent(text?: string | null): void;
        /** Execute vscode command <command_id> with return value */
        vscode_get(command_id: string, arg1?: any, arg2?: any, arg3?: any, arg4?: any, arg5?: any): any;
        /** Get the value of vscode setting at the given key */
        vscode_get_setting(key: string, default_value?: any): void;
        /** Returns a vscode setting with a fallback in case there's an error

        Args:
            key (str): The key of the setting to look up
            default_value (Any): The default value to return if the setting is not defined
            fallback_value (Any): The value to return if there is an error looking up the setting
            fallback_message (str): The message to show to the user if we end up having to use the fallback

        Returns:
            tuple[Any, bool]: The value of the setting or the default or fall back, along with boolean which is true if there was an error */
        vscode_get_setting_with_fallback(key: string, default_value: any, fallback_value: any, fallback_message: string): [any, boolean];
        /** Get path of vscode settings json file */
        vscode_settings_path(): Path;
        /** Take word on cursorless target with number of repeats */
        vscode_take_word(cursorless_target: Record<string, any>, repeats: number): void;
        /** Execute command via vscode command server. */
        vscode_with_plugin(command_id: string, arg1?: any, arg2?: any, arg3?: any, arg4?: any, arg5?: any): void;
        /** Execute command via vscode command server and wait for command to finish. */
        vscode_with_plugin_and_wait(command_id: string, arg1?: any, arg2?: any, arg3?: any, arg4?: any, arg5?: any): void;
        /** Watch csv file for changes. Present content as dict */
        watch_csv_as_dict(path: Path, callback: (arg0: Record<string, any>) => null, values_as_list?: boolean): void;
        /** Watch csv file for changes. Present content as list */
        watch_csv_as_list(path: Path, callback: (arg0: string[][], arg1: string[]) => null): void;
        /** Switch focus to last window */
        window_focus_last(): void;
        /** Focus application named <name> */
        window_focus_name(name: string, phrase?: Phrase): void;
        /** Resize the active window */
        window_resize(side: string, direction: string, offset: string): void;
        /** Update window position. Keeps track of old position to enable revert/undo */
        window_set_pos(window: Window, x: number, y: number, width: number, height: number): void;
        /** Update window position. Keeps track of old position to enable revert/undo */
        window_set_rect(window: Window, rect: Rect): void;
        /** Show window switcher menu */
        window_switcher_menu(): void;
    };
}
