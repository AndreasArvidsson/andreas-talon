from talon import Module, settings
from talon.grammar import Phrase

mod = Module()

settings_log = mod.setting(
    "print_phrase_timings",
    type=bool,
    default=False,
    desc="If true phrase timings will be printed to the log",
)


def print_phrase_timings(phrase: Phrase):
    """Print phrase timings"""
    if not settings.get("user.print_phrase_timings"):
        return
    try:
        meta = phrase["_metadata"]
        status = f"[audio]={meta['audio_ms']:.3f}ms "
        status += f"[compile]={meta['compile_ms']:.3f}ms "
        status += f"[emit]={meta['emit_ms']:.3f}ms "
        status += f"[decode]={meta['decode_ms']:.3f}ms "
        status += f"[total]={meta['total_ms']:.3f}ms "
        print(" ".join(phrase["phrase"]))
        print(status)
    except KeyError:
        pass
