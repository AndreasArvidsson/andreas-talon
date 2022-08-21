from talon import Module, actions, scope
from talon.grammar import Phrase

mod = Module()

settings_log = mod.setting(
    "timings_log",
    type=bool,
    default=False,
    desc="If true phrase timings will be printed to the log",
)

# These contains the actual spoken phrase. Removed to not get a keylogger.
blacklist = {"emit", "decode"}


@mod.action_class
class Actions:
    def print_phrase_timings(phrase: Phrase, text: str):
        """Print phrase timings"""
        try:
            meta = phrase["_metadata"]

            scope_app = scope.get("app.app")

            actions.user.persist_append(
                "phrase",
                {
                    "application": ", ".join(scope_app) if scope_app else None,
                    **{k: v for k, v in meta.items() if k not in blacklist},
                },
            )

            if settings_log.get():
                status = f"[audio]={meta['audio_ms']:.3f}ms "
                status += f"[compile]={meta['compile_ms']:.3f}ms "
                status += f"[emit]={meta['emit_ms']:.3f}ms "
                status += f"[decode]={meta['decode_ms']:.3f}ms "
                status += f"[total]={meta['total_ms']:.3f}ms "
                print(text)
                print(status)
        except KeyError:
            pass
