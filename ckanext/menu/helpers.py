from __future__ import annotations

from markupsafe import Markup

import ckan.plugins.toolkit as tk

import ckanext.menu.utils as menu_utils


def build_menu_tree(menu_name, snippet=None, start=0, end=None):
    tree = menu_utils.menu_build_ordered_tree(menu_name, start, end)

    if tree:
        template = snippet if snippet else "menu/snippets/menu_list.html"
        return Markup(
            tk.render(
                template,
                extra_vars={"tree": tree},
            )
        )

    return Markup("")


def build_top_menu_tree(menu_name, snippet=None):
    tree = menu_utils.top_levels_links(menu_name)

    if tree:
        template = snippet if snippet else "menu/snippets/menu_list.html"
        return Markup(
            tk.render(
                template,
                extra_vars={"tree": tree},
            )
        )

    return Markup("")


def menu_has_active_descendant(item):
    if item.get("active"):
        return True
    for child in item.get("children", []):
        if menu_has_active_descendant(child):
            return True
    return False


def menu_item_translation(menu_item, field='title'):
    if isinstance(menu_item, dict):
        translations = menu_item.get("translations")
    else:
        menu_item = menu_item.dictize({})
        translations = menu_item.translations

    text = menu_item.get(field, "")

    if translations:
        lang = tk.h.lang()
        if lang in translations:
            data = translations[lang]
            if field in data and data[field]:
                text = data[field]

    return text
