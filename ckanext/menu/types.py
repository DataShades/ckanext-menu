from __future__ import annotations

from typing import TypedDict, Any


class MenuItem(TypedDict):
    id: str
    title: str
    url: str
    order: int
    pid: str | None
    classes: str | None
    attributes: str | None
    mid: str
    translations: dict[str, Any]


class Menu(TypedDict):
    id: str
    name: str
    items: list[MenuItem]
    created: str
    modified: str
