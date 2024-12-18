from typing import Literal, TypedDict


class ReadBookmark(TypedDict):
    title: str
    url: str


class ClipItemMeta(TypedDict):
    src: str | None
    alt: str | None


class ClipItem(TypedDict):
    id: str
    created: int
    type: Literal["text", "image"]
    name: str | None
    list: str | None
    text: str | None
    rtf: str | None
    html: str | None
    image: str | None
    bookmark: ReadBookmark | None
    meta: ClipItemMeta | None
