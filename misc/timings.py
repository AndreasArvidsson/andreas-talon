from talon import Module

mod = Module()


@mod.action_class
class Actions:
    def print_phrase_timings(phrase: dict):
        """Print phrase timings"""
        try:
            meta = phrase["_metadata"]
            status = f"[audio]={meta['audio_ms']:.3f}ms "
            status += f"[compile]={meta['compile_ms']:.3f}ms "
            status += f"[emit]={meta['emit_ms']:.3f}ms "
            status += f"[decode]={meta['decode_ms']:.3f}ms "
            status += f"[total]={meta['total_ms']:.3f}ms "
            print(status)
        except KeyError:
            pass
