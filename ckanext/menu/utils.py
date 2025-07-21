from __future__ import annotations

import json
import logging
from urllib.parse import urlparse

import ckan.plugins.toolkit as tk

from ckanext.menu.model.menu import CKANMenuItemModel, CKANMenuModel

log = logging.getLogger(__name__)


def menu_build_ordered_tree(menu_name, start=0, end=None):
    menu = CKANMenuModel.get_by_name(menu_name)
    tree = []

    if menu:
        menu_items = CKANMenuItemModel.get_by_menu_id(menu.id)

        # Step 1: Prepare dicts list
        item_dicts = [obj.dictize({}) for obj in menu_items]

        # Step 2: Build a mapping by id
        items_by_id = {item["id"]: item for item in item_dicts}

        # Step 3: Build the tree structure
        for item in item_dicts:
            pid = item["pid"]
            if pid is not None and pid in items_by_id:
                if "children" not in items_by_id[pid]:
                    items_by_id[pid]["children"] = []
                items_by_id[pid]["children"].append(item)
            else:
                tree.append(item)

        def tree_levels(ttree, current_level, start_level=0, end_level=None):
            def truncate_depth(ltree, lcurrent_level, max_level):
                """Recursively trims the tree beyond max_level."""
                if lcurrent_level >= max_level:
                    for node in ltree:
                        node.pop("children", None)
                    return ltree
                for node in ltree:
                    if "children" in node:
                        truncate_depth(node["children"], lcurrent_level + 1, max_level)
                return ltree

            # First, truncate tree to a max depth if end > 0
            if end_level is not None:
                if end_level == 0 or end_level > 0:
                    ttree = truncate_depth(ttree, 0, end_level)

            if current_level < start_level:
                temp_tree = [
                    child for i in ttree if i.get("children") for child in i["children"]
                ]

                return tree_levels(temp_tree, current_level + 1, start_level, None)
            else:
                return ttree

        tree = tree_levels(tree, 0, start, end)

        current_path = tk.request.path
        current_host = tk.request.host

        # Step 4: Sort recursively by 'order'
        def sort_recursive(m_items):
            m_items.sort(key=lambda x: x["order"])
            for m_item in m_items:
                parsed = urlparse(m_item.get("url") or "")
                item_host = parsed.netloc
                item_path = parsed.path

                # Only check path if host matches or not specified
                if not item_host or item_host == current_host:
                    if item_path == current_path or item_path + "/" == current_path:
                        m_item["active"] = True
                        m_item["classes"] = (m_item.get("classes") or "") + " active"
                if m_item.get("attributes"):
                    attributes = m_item.get("attributes")
                    try:
                        m_item["attributes"] = json.loads(attributes)
                    except json.JSONDecodeError:
                        m_item.pop("attributes")
                        log.error(
                            "Cannot load json for menu item '%s'.", m_item["title"]
                        )

                m_item['title'] = tk.h.menu_item_translation(m_item)
                sort_recursive(m_item.get("children", []))

        sort_recursive(tree)

    return tree


def top_levels_links(menu_name):
    menu = CKANMenuModel.get_by_name(menu_name)
    if menu:
        links = CKANMenuItemModel.get_top_level_by_menu_id(menu.id)
        links = [obj.dictize({}) for obj in links]
        return links
