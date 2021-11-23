from talon import Module

mod = Module()
debug_timings_setting = mod.setting("debug_timings", bool, default=False)


@mod.action_class
class Actions:
    def print_phrase_timings(phrase: dict, text: str):
        """Print phrase timings"""
        if not debug_timings_setting.get():
            return
        try:
            meta = phrase["_metadata"]
            status = f"[audio]={meta['audio_ms']:.3f}ms "
            status += f"[compile]={meta['compile_ms']:.3f}ms "
            status += f"[emit]={meta['emit_ms']:.3f}ms "
            status += f"[decode]={meta['decode_ms']:.3f}ms "
            status += f"[total]={meta['total_ms']:.3f}ms "
            print(text)
            print(status)
        except KeyError:
            pass
