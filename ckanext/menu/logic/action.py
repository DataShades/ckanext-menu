from __future__ import annotations

from typing import cast

import ckan.plugins.toolkit as tk
from ckan import types
from ckan.logic import validate

import ckanext.menu.logic.schema as schema
from ckanext.menu.model.menu import CKANMenuModel, CKANMenuItemModel
import ckanext.menu.types as menu_types


@validate(schema.menu_create)
def menu_create(context: types.Context, data_dict: types.DataDict) -> menu_types.Menu:
    tk.check_access("menu_create", context, data_dict)

    menu = CKANMenuModel.create(data_dict)

    return menu.dictize(context)


@validate(schema.menu_item_create)
def menu_item_create(
    context: types.Context, data_dict: types.DataDict
) -> menu_types.MenuItem:
    tk.check_access("menu_item_create", context, data_dict)

    menu_item = CKANMenuItemModel.create(data_dict)

    return menu_item.dictize(context)


@tk.side_effect_free
def menus_list(
    context: types.Context, data_dict: types.DataDict
) -> list[menu_types.Menu]:
    tk.check_access("menu_view", context, data_dict)

    return [menu.dictize(context) for menu in CKANMenuModel.get_all()]


@validate(schema.menu_edit)
def menu_edit(context: types.Context, data_dict: types.DataDict) -> menu_types.Menu:
    tk.check_access("menu_edit", context, data_dict)

    menu = CKANMenuModel.get_by_id(data_dict["id"])

    if not menu:
        raise tk.ObjectNotFound("Menu not found")

    menu.update(data_dict)

    return menu.dictize(context)


@validate(schema.menu_item_edit)
def menu_item_edit(
    context: types.Context, data_dict: types.DataDict
) -> menu_types.MenuItem:
    tk.check_access("menu_edit", context, data_dict)

    menu_item = CKANMenuItemModel.get_by_id(data_dict["id"])

    if not menu_item:
        raise tk.ObjectNotFound("Menu Item not found")

    menu_item.update(data_dict)

    return menu_item.dictize(context)


@validate(schema.menu_delete)
def menu_delete(
    context: types.Context, data_dict: types.DataDict
) -> types.ActionResult.AnyDict:
    tk.check_access("menu_delete", context, data_dict)

    menu = cast(CKANMenuModel, CKANMenuModel.get_by_id(data_dict["id"]))

    menu.delete()

    return {"success": True}


@validate(schema.menu_item_delete)
def menu_item_delete(
    context: types.Context, data_dict: types.DataDict
) -> types.ActionResult.AnyDict:
    tk.check_access("menu_item_delete", context, data_dict)

    menu_item = CKANMenuItemModel.get_by_id(data_dict["id"])

    if menu_item:
        menu_item.delete()

        children = CKANMenuItemModel.get_menu_items_by_pid(data_dict["id"])
        for child in children:
            _delete_menu_item_children(child)

    return {"success": True}


def _delete_menu_item_children(child):
    children = CKANMenuItemModel.get_menu_items_by_pid(str(child.id))
    if children:
        for c in children:
            _delete_menu_item_children(c)

    child.delete()


def menu_items_update_order(
    context: types.Context, data_dict: types.DataDict
) -> types.ActionResult.AnyDict:
    tk.check_access("menu_edit", context, data_dict)

    data = data_dict.get("data")

    if data:
        for item_dict in data:
            menu_item = CKANMenuItemModel.get_by_id(item_dict["id"])
            if menu_item:
                try:
                    if menu_item.pid != item_dict["pid"]:
                        menu_item.update(
                            {
                                "pid": item_dict["pid"],
                                "order": item_dict["order"],
                            }
                        )
                except Exception as e:
                    return {"success": False, "error": str(e)}

    return {"success": True}
