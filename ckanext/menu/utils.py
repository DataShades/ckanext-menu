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

    # Step 4: Sort recursively by 'order'
    def sort_recursive(m_items):
        m_items.sort(key=lambda x: x["order"])
        for m_item in m_items:
            sort_recursive(m_item.get("children", []))

    sort_recursive(tree)
    return tree
