from talon import Context, Module

mod = Module()
ctx = Context()

mod.list("webpage", desc="List of webpages")

ctx.lists["self.webpage"] = {
    "github":               "https://github.com",
    "talon slack":          "https://talonvoice.slack.com",
    "regex cheat sheet":    "https://duckduckgo.com/?q=regex+cheat+sheet&t=ffab&ia=cheatsheet&iax=1",
    "avanza":               "https://www.avanza.se",
    "savr":                 "https://www.savr.com",
    "swedbank":             "https://swedbank.se",
    "sweclockers":          "https://www.sweclockers.com/forum/aktiva",
    "goodreads":            "https://www.goodreads.com",
    "gmail":                "https://www.gmail.com",
    "youtube":              "https://www.youtube.com/feed/subscriptions",
    "facebook":             "https://www.facebook.com",
    "audible":              "https://www.audible.co.uk",
    "calendar":             "https://calendar.google.com",
    "news":                 "https://www.svt.se",
    "dropbox":              "https://www.dropbox.com",
    "imdb":                 "https://www.imdb.com",
    "kbab":                 "https://kbab.se/mina-sidor",
    "linkedin":             "https://www.linkedin.com",
    "prisjakt":             "https://classic.prisjakt.nu",
    "pricerunner":          "https://www.pricerunner.se",

    # Redpill Linpro & customers
    "zimbra":               "https://zimbra.redpill-linpro.com",
    "redmine":              "https://redmine.redpill-linpro.com",
    "mattermost":           "https://mattermost.redpill-linpro.com",
    "gitlab":               "https://gitlab.redpill-linpro.com",
    "redpill info":         "https://info.redpill-linpro.com",
    "bitbucket":            "https://bitbucket.org",
    "xledger":              "https://xledger.net",
    "business manager":     "https://payroll.accountor.se",
    "patientenkaet":        "https://patientenkat.se",
    "ppm":                  "https://ppm.vantetider.se",
    "hassan":               "https://app.vantetider.se/hassan"
}