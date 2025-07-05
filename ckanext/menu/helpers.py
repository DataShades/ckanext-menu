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
