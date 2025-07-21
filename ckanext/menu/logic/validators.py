from __future__ import annotations

from typing import Any
from urllib.parse import ParseResult, urlparse
import re
import json

import ckan.plugins.toolkit as tk
import ckan.types as types

from ckanext.menu.model.menu import CKANMenuItemModel, CKANMenuModel


def menu_exist(menu_id: str, context: types.Context) -> Any:
    """Ensures that the menu with a given id exists"""

    if not CKANMenuModel.get_by_id(menu_id):
        raise tk.Invalid(f"The menu {menu_id} doesn't exist.")

    return menu_id


def menu_item_exist(menu_item_id: str, context: types.Context) -> Any:
    """Ensures that the menu with a given id exists"""

    if not CKANMenuItemModel.get_by_id(menu_item_id):
        raise tk.Invalid(f"The menu {menu_item_id} doesn't exist.")

    return menu_item_id


def pid_menu_item_exist(
    key: types.FlattenKey,
    data: types.FlattenDataDict,
    errors: types.FlattenErrorDict,
    context: types.Context,
) -> Any:
    """Ensures that the menu item with a given id exists in the same menu"""

    menu_id = data.get(("menu_id",))
    parent_menu_item_id = data.get(("parent_id",))

    if not menu_id or not parent_menu_item_id:
        return

    current_menu = CKANMenuModel.get_by_id(menu_id)
    parent_menu_item = CKANMenuItemModel.get_by_id(parent_menu_item_id)

    if not parent_menu_item:
        raise tk.Invalid(f"The menu item {parent_menu_item_id} doesn't exist.")

    if not current_menu:
        return

    if parent_menu_item.menu_id != current_menu.id:
        raise tk.Invalid(
            f"The menu item {parent_menu_item_id} doesn't exist in the same menu."
        )


def menu_name_is_unique(
    key: types.FlattenKey,
    data: types.FlattenDataDict,
    errors: types.FlattenErrorDict,
    context: types.Context,
) -> Any:
    """Ensures that the name with a given name doesn't exist"""

    val = data[key]
    id = data.get(("id",))
    menu = CKANMenuModel.get_by_name(val)
    if menu:
        if not id:
            raise tk.Invalid(f"The name {val} already exists.")

        if int(id) != menu.id:
            raise tk.Invalid(f"The name {val} already exists.")

    return


def menu_item_url_unique(
    key: types.FlattenKey,
    data: types.FlattenDataDict,
    errors: types.FlattenErrorDict,
    context: types.Context,
) -> Any:
    """Ensures that the given url doesn't exist"""
    val = data[key]
    id = data.get(("id",))

    if not val:
        return

    if id:
        current_content = CKANMenuItemModel.get_by_id(id)
        if current_content and val == current_content.url:
            return
    else:
        content = CKANMenuItemModel.get_by_url(val)
        if content:
            raise tk.Invalid(f"Such url already exists.")

    return


def menu_is_valid_url(
    key: types.FlattenKey,
    data: types.FlattenDataDict,
    errors: types.FlattenErrorDict,
    context: types.Context,
) -> Any:
    """Ensures that the given value is an relative path with leading slash or https"""
    value = data[key]

    if not isinstance(value, str):
        errors[key].append("Must be a string.")

    if value.startswith("http"):
        try:
            r: ParseResult = urlparse(value)
            if not all([r.scheme, r.netloc]):
                errors[key].append("Not a valid URL.")
        except Exception:
            errors[key].append("Not a valid URL.")
    elif value == "<no_link>":
        return
    else:
        if not value.startswith("/") or value.startswith("//"):
            errors[key].append(
                "Must start with a single slash (/) and not with // or without slashes at all."
            )

        if not re.fullmatch(r"/[A-Za-z0-9][A-Za-z0-9_\-/]*", value):
            errors[key].append(
                'Path must start with a slash followed by a letter or digit, and contain only letters, digits, "-", or "_".'
            )

        if value.endswith("/"):
            errors[key].append('Should not end with "/".')

    return


def menu_valid_json(
    key: types.FlattenKey,
    data: types.FlattenDataDict,
    errors: types.FlattenErrorDict,
    context: types.Context,
) -> Any:
    val = data.get(key)
    if val:
        try:
            json.loads(val)
        except json.JSONDecodeError:
            errors[key].append("Not a valid JSON.")
    return
