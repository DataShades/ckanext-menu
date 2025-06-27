from markupsafe import Markup

import ckan.plugins.toolkit as tk

from ckanext.menu.model.menu import CKANMenuItemModel, CKANMenuModel
import ckanext.menu.utils as menu_utils


def build_menu_tree(menu_name, snippet=None):
    menu = CKANMenuModel.get_by_name(menu_name)

    if menu:
        menu_items = CKANMenuItemModel.get_by_menu_id(str(menu.id))

        tree = menu_utils.menu_build_ordered_tree(menu_items)

        template = snippet if snippet else "menu/snippets/menu_list.html"
        return Markup(
            tk.render(
                template,
                extra_vars={"tree": tree},
            )
        )

    return Markup("")
