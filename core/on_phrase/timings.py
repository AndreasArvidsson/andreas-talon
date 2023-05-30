from talon import Module
from talon.grammar import Phrase

mod = Module()

settings_log = mod.setting(
    "timings_log",
    type=bool,
    default=False,
    desc="If true phrase timings will be printed to the log",
)


@mod.action_class
class Actions:
    def print_phrase_timings(phrase: Phrase):
        """Print phrase timings"""
        try:
            meta = phrase["_metadata"]

            if settings_log.get():
                status = f"[audio]={meta['audio_ms']:.3f}ms "
                status += f"[compile]={meta['compile_ms']:.3f}ms "
                status += f"[emit]={meta['emit_ms']:.3f}ms "
                status += f"[decode]={meta['decode_ms']:.3f}ms "
                status += f"[total]={meta['total_ms']:.3f}ms "
                print(" ".join(phrase["phrase"]))
                print(status)
        except KeyError:
            pass
