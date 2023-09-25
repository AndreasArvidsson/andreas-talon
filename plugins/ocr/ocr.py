import functools
import operator
from talon import Module, ui, screen, cron, Context
from talon.experimental import ocr
from talon.experimental.ocr import Result
from talon.canvas import Canvas
from talon.types import Rect
import re
import time

mod = Module()
ctx = Context()
ocr_result: list[Result] = []

mod.list("ocr_text")


@ctx.dynamic_list("user.ocr_text")
def ocr_text() -> str:
    global ocr_result
    ocr_result = ocr_window()
    return ocr_result_to_string(ocr_result)


@mod.action_class
class Actions:
    def ocr(text: str):
        """ocr"""
        print(text)

        for result in ocr_result:
            # print(rect)
            # print(image.rect)

            # for match in re.finditer(r"\S+", result.text):
            for match in re.finditer(text, result.text):
                print("----------")
                print(result.text)
                print(match)
                # a|whatever|b
                start = result.bounds.rects[match.start()]
                end = result.bounds.rects[match.end() - 1]
                rect = start + end
                # rect = Rect(
                #     start.x - image.rect.x,
                #     start.y - image.rect.y,
                #     end.right - start.left,
                #     start.height,
                # )
                # print(start, end)
                # print(rect)
                flash_rect(rect)
                # rects = result.bounds.rects[match.start() : match.end() - 1]

                # a = functools.reduce(
                #     operator.add,
                #     result.bounds.rects[match.start() : match.end()],
                # )
                # print(rect)
                # print(a)
                # print("--")

                # for i, r in enumerate(result.bounds.rects):
                #     if i == match.start():
                #         print("[")
                #     print(r)
                #     if i == match.end() - 1:
                #         print("]")

                # print(len(r.text))

                # break


def ocr_result_to_string(result: list[Result]) -> str:
    content = ""

    for result in ocr_result:
        content += re.sub(r"[^a-zA-Z]+", " ", result.text)
        content += " "

    return content


def ocr_window() -> list[Result]:
    win = ui.active_window()
    return ocr_rect(win.rect)


def ocr_rect(rect: ui.Rect) -> list[Result]:
    image = screen.capture_rect(rect)
    return ocr.ocr(image)


def flash_rect(rect: ui.Rect):
    def on_draw(c):
        c.paint.style = c.paint.Style.FILL
        c.paint.color = "ff0000"
        c.draw_rect(rect)
        cron.after("5s", canvas.close)

    canvas = Canvas.from_rect(rect)
    canvas.register("draw", on_draw)
    canvas.freeze()
