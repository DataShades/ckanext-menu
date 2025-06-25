from __future__ import annotations

from typing import Any, Dict

from ckan.logic.schema import validator_args

Schema = Dict[str, Any]


@validator_args
def menu_create(
    not_empty,
    unicode_safe,
    name_validator,
    ignore_empty,
    ignore,
    menu_name_is_unique,
) -> Schema:
    return {
        "title": [not_empty, unicode_safe],
        "name": [not_empty, unicode_safe, name_validator, menu_name_is_unique],
        "__extras": [ignore_empty, ignore],
    }


@validator_args
def menu_item_create(
    not_empty,
    unicode_safe,
    default,
    int_validator,
    ignore_empty,
    ignore,
    pid_menu_item_exist,
    menu_exist,
    menu_is_valid_url,
) -> Schema:
    return {
        "title": [not_empty, unicode_safe],
        "url": [not_empty, unicode_safe, menu_is_valid_url],
        "order": [default(0), int_validator],
        "pid": [ignore_empty, unicode_safe, pid_menu_item_exist],
        "classes": [ignore_empty, unicode_safe],
        "mid": [not_empty, unicode_safe, menu_exist],
        "__extras": [ignore],
    }


@validator_args
def menu_edit(
    not_empty,
    unicode_safe,
    name_validator,
    ignore_empty,
    ignore,
    menu_exist,
    menu_name_is_unique,
) -> Schema:
    return {
        "id": [not_empty, unicode_safe, menu_exist],
        "title": [not_empty, unicode_safe],
        "name": [not_empty, unicode_safe, name_validator, menu_name_is_unique],
        "__extras": [ignore_empty, ignore],
    }


@validator_args
def menu_item_edit(
    not_empty,
    unicode_safe,
    default,
    int_validator,
    ignore_empty,
    ignore,
    pid_menu_item_exist,
    menu_exist,
    menu_item_exist,
    menu_is_valid_url,
) -> Schema:
    return {
        "id": [not_empty, unicode_safe, menu_item_exist],
        "title": [not_empty, unicode_safe],
        "url": [not_empty, unicode_safe, menu_is_valid_url],
        "order": [default(0), int_validator],
        "pid": [ignore_empty, unicode_safe, pid_menu_item_exist],
        "classes": [ignore_empty, unicode_safe],
        "mid": [not_empty, unicode_safe, menu_exist],
        "__extras": [ignore],
    }


@validator_args
def menu_delete(not_empty, unicode_safe, menu_exist) -> Schema:
    return {"id": [not_empty, unicode_safe, menu_exist]}


@validator_args
def menu_item_delete(not_empty, unicode_safe, menu_item_exist) -> Schema:
    return {"id": [not_empty, unicode_safe, menu_item_exist]}
