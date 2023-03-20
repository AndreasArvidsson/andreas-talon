from talon import Context, Module

mod = Module()
ctx = Context()

mod.list("webpage", desc="List of webpages")

# fmt: off

ctx.lists["self.webpage"] = {
    "audible":              "https://www.audible.co.uk",
    "avanza":               "https://www.avanza.se",
    "calendar":             "https://calendar.google.com",
    "cursorless":           "https://cursorless.org",
    "dropbox":              "https://www.dropbox.com",
    "facebook":             "https://www.facebook.com",
    "github":               "https://github.com",
    "gmail":                "https://www.gmail.com",
    "goodreads":            "https://www.goodreads.com",
    "imdb":                 "https://www.imdb.com",
    "karlstad buss":        "https://www.karlstadsbuss.se",
    "kbab":                 "https://minasidor.kbab.se",
    "kivra":                "https://www.kivra.se",
    "komplett bank":        "https://www.komplettbank.se",
    "linkedin":             "https://www.linkedin.com",
    "news":                 "https://www.svt.se",
    "nine gag":             "https://9gag.com",
    "pricerunner":          "https://www.pricerunner.se",
    "prisjakt":             "https://classic.prisjakt.nu",
    "regex cheat sheet":    "https://duckduckgo.com/?q=regex+cheat+sheet&t=ffab&ia=cheatsheet&iax=1",
    "regex one oh one":     "https://regex101.com",
    "savr":                 "https://www.savr.com",
    "swec":                 "https://www.sweclockers.com/forum/aktiva",
    "sweclockers":          "https://www.sweclockers.com/forum/aktiva",
    "swedbank":             "https://swedbank.se",
    "talon deck":           "http://localhost:3000",
    "talon noise":          "https://noise.talonvoice.com",
    "talon search":         "https://search.talonvoice.com",
    "talon slack":          "https://talonvoice.slack.com",
    "talon speech":         "https://speech.talonvoice.com",
    "youtube":              "https://www.youtube.com/feed/subscriptions",

    # Redpill Linpro & customers
    "bitbucket":            "https://bitbucket.org",
    "cv partner":           "https://redpill-linpro.cvpartner.com",
    "gitlab":               "https://gitlab.redpill-linpro.com",
    "hassan":               "https://app.vantetider.se/hassan",
    "hogia business":       "https://payroll.accountor.se",
    "mattermost":           "https://mattermost.redpill-linpro.com",
    "patientenkaet":        "https://patientenkat.se",
    "ppm":                  "https://ppm.vantetider.se",
    "redmine":              "https://redmine.redpill-linpro.com",
    "redpill info":         "https://info.redpill-linpro.com",
    "teams":                "https://teams.microsoft.com",
    "vpn":                  "vpn.redpill-linpro.com",
    "wildly tunnel":        "http://localhost:10190",
    "xledger":              "https://xledger.net",
    "zimbra":               "https://zimbra.redpill-linpro.com",
}
