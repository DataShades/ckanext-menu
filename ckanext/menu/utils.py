import json
from urllib.parse import urlparse

import ckan.plugins.toolkit as tk


def menu_build_ordered_tree(objects):
    # Step 1: Prepare dicts list
    item_dicts = [obj.dictize({}) for obj in objects]

    # Step 2: Build a mapping by id
    items_by_id = {item["id"]: item for item in item_dicts}

    # Step 3: Build the tree structure
    tree = []
    for item in item_dicts:
        pid = item["pid"]
        if pid is not None and pid in items_by_id:
            if "children" not in items_by_id[pid]:
                items_by_id[pid]["children"] = []
            items_by_id[pid]["children"].append(item)
        else:
            tree.append(item)

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
                if "'" in attributes:
                    attributes = attributes.replace("'", '"')
                try:
                    m_item["attributes"] = json.loads(attributes)
                except json.JSONDecodeError as e:
                    pass

            sort_recursive(m_item.get("children", []))

    sort_recursive(tree)

    return tree
