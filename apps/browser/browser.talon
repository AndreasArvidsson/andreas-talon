tag: browser
-
tag(): user.zoom
tag(): user.tabs
tag(): user.find
tag(): user.navigation

go address:                 browser.focus_address()
go home:                    browser.go_home()
go {user.webpage}:          browser.go(webpage)
open {user.webpage}:        user.browser_open(webpage)

go private:                 browser.open_private_window()

bookmark show:              browser.bookmarks()
bookmark bar:               browser.bookmarks_bar()
bookmark it:                browser.bookmark()
bookmark tabs:              browser.bookmark_tabs()

(refresh | reload) page:    browser.reload()
(refresh | reload) page hard: browser.reload_hard()

show downloads:             browser.show_downloads()
show extensions:            browser.show_extensions()
show history:               browser.show_history()
show cache:                 browser.show_clear_cache()

dev tools:                  browser.toggle_dev_tools()

fullscreen:                 key(f)
