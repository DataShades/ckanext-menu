from __future__ import annotations

import ckan.plugins.toolkit as tk
from ckan.types import AuthResult, Context, DataDict

from ckanext.menu.model.menu import CKANMenuModel, CKANMenuItemModel


def menu_list(context: Context, data_dict: DataDict) -> AuthResult:
    return {"success": False}


@tk.auth_allow_anonymous_access
def menu_view(context: Context, data_dict: DataDict) -> AuthResult:
    mid = tk.get_or_bust(data_dict, "id")

    menu = CKANMenuModel.get_by_id(mid)

    if not menu:
        return {"success": False}

    return {"success": True}


def menu_create(context: Context, data_dict: DataDict) -> AuthResult:
    return {"success": False}


def menu_edit(context: Context, data_dict: DataDict) -> AuthResult:
    return {"success": False}


def menu_delete(context: Context, data_dict: DataDict) -> AuthResult:
    return {"success": False}


@tk.auth_allow_anonymous_access
def menu_list_view(context: Context, data_dict: DataDict) -> AuthResult:
    mid = tk.get_or_bust(data_dict, "id")

    menu_item = CKANMenuItemModel.get_by_id(mid)

    if not menu_item:
        return {"success": False}

    return {"success": True}


def menu_item_create(context: Context, data_dict: DataDict) -> AuthResult:
    return {"success": False}


def menu_item_edit(context: Context, data_dict: DataDict) -> AuthResult:
    return {"success": False}


def menu_item_delete(context: Context, data_dict: DataDict) -> AuthResult:
    return {"success": False}
