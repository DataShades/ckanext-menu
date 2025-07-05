from __future__ import annotations

from flask import Blueprint
from flask.views import MethodView


import ckan.lib.navl.dictization_functions as dict_fns
import ckan.logic as logic
import ckan.plugins.toolkit as tk
from ckan.types import Context

from ckanext.menu.model.menu import CKANMenuModel, CKANMenuItemModel
import ckanext.menu.utils as m_utils


ValidationError = logic.ValidationError

menu_item = Blueprint("menu_item", __name__)


def make_context() -> Context:
    return {
        "user": tk.current_user.name,
        "auth_user_obj": tk.current_user,
    }


class CreateView(MethodView):
    def get(self, mid: str):
        try:
            tk.check_access("menu_item_create", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        try:
            form_data = logic.clean_dict(
                dict_fns.unflatten(
                    logic.tuplize_dict(logic.parse_params(tk.request.form))
                )
            )
        except dict_fns.DataError:
            return tk.base.abort(400, tk._("Integrity Error"))

        menu_items = CKANMenuItemModel.get_by_menu_id(mid)

        pid_options = [{"value": m.id, "text": m.title} for m in menu_items]
        pid_options = [{"value": "", "text": "None"}, *pid_options]

        extra_vars = {
            "mid": mid,
            "pid_options": pid_options,
            "form_data": form_data,
            "errors": {},
        }

        return tk.render("menu/menu_item/create.html", extra_vars=extra_vars)

    def post(self, mid: str):
        try:
            tk.check_access("menu_item_create", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        try:
            form_data = logic.clean_dict(
                dict_fns.unflatten(
                    logic.tuplize_dict(logic.parse_params(tk.request.form))
                )
            )
        except dict_fns.DataError:
            return tk.base.abort(400, tk._("Integrity Error"))

        form_data["mid"] = mid
        try:
            tk.get_action("menu_item_create")(make_context(), form_data)
        except logic.ValidationError as e:
            tk.h.flash_error(e.error_summary)

            menu_items = CKANMenuItemModel.get_by_menu_id(mid)

            pid_options = [{"value": m.id, "text": m.title} for m in menu_items]
            pid_options = [{"value": "", "text": "None"}, *pid_options]

            extra_vars = {
                "mid": mid,
                "pid_options": pid_options,
                "form_data": form_data,
                "errors": {},
            }

            return tk.render(
                "menu/menu_item/create.html",
                extra_vars=extra_vars,
            )

        return tk.redirect_to("menu_item.list", mid=mid)


class EditView(MethodView):
    def get(self, mid: str, id: str):
        menu_item = CKANMenuItemModel.get_by_id(id)

        try:
            tk.check_access("menu_edit", make_context(), {"id": id})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        if not menu_item:
            return tk.abort(404, "Page not found")

        form_data = menu_item.dictize({})

        menu_items = CKANMenuItemModel.get_by_menu_id(mid)

        pid_options = [{"value": m.id, "text": m.title} for m in menu_items]
        pid_options = [{"value": "", "text": "None"}, *pid_options]

        extra_vars = {
            "id": id,
            "mid": mid,
            "pid_options": pid_options,
            "form_data": form_data,
            "errors": {},
        }

        return tk.render(
            "menu/menu_item/edit.html",
            extra_vars=extra_vars,
        )

    def post(self, mid: str, id: str):
        try:
            tk.check_access("menu_item_edit", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        try:
            form_data = logic.clean_dict(
                dict_fns.unflatten(
                    logic.tuplize_dict(logic.parse_params(tk.request.form))
                )
            )
        except dict_fns.DataError:
            return tk.base.abort(400, tk._("Integrity Error"))

        form_data["id"] = id
        form_data["mid"] = mid

        menu_items = CKANMenuItemModel.get_by_menu_id(mid)

        pid_options = [{"value": m.id, "text": m.title} for m in menu_items]
        pid_options = [{"value": "", "text": "None"}, *pid_options]

        try:
            tk.get_action("menu_item_edit")(make_context(), form_data)
        except logic.ValidationError as e:
            tk.h.flash_error(e.error_summary)
            extra_vars = {
                "id": id,
                "mid": mid,
                "pid_options": pid_options,
                "form_data": form_data,
                "errors": {},
            }

            return tk.render(
                "menu/menu_item/edit.html",
                extra_vars=extra_vars,
            )

        return tk.redirect_to("menu_item.list", mid=mid)


class ListView(MethodView):
    def get(self, mid: str):
        try:
            tk.check_access("menu_item_create", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        menu = CKANMenuModel.get_by_id(mid)
        menu_items = CKANMenuItemModel.get_by_menu_id(int(mid))

        tree = m_utils.menu_build_ordered_tree(menu.name)

        extra_vars = {
            "menu_items": menu_items,
            "menu": menu,
            "tree": tree,
        }

        return tk.render("menu/menu_item/list.html", extra_vars=extra_vars)


class DeleteView(MethodView):
    def get(self, mid: str, id: str):
        menu_item = CKANMenuItemModel.get_by_id(id)

        try:
            tk.check_access("menu_item_delete", make_context(), {"id": id})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        if not menu_item:
            return tk.abort(404, "Page not found")

        form_data = menu_item.dictize({})

        return tk.render(
            "menu/menu_item/delete.html",
            extra_vars={
                "id": id,
                "form_data": form_data,
                "errors": {},
            },
        )

    def post(self, mid: str, id: str):
        try:
            tk.check_access("menu_item_delete", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        form_data = {"id": id}

        try:
            tk.get_action("menu_item_delete")(make_context(), form_data)
        except logic.ValidationError as e:
            tk.h.flash_error(e.error_summary)
            return tk.render(
                "menu/menu_item/delete.html",
                extra_vars={"form_data": form_data, "errors": {}},
            )

        return tk.redirect_to("menu_item.list", mid=mid)


menu_item.add_url_rule(
    "/menu/<mid>/menu-item/create", view_func=CreateView.as_view("create")
)
menu_item.add_url_rule(
    "/menu/<mid>/menu-item/<id>/edit", view_func=EditView.as_view("edit")
)
menu_item.add_url_rule(
    "/menu/<mid>/menu-item/<id>/delete", view_func=DeleteView.as_view("delete")
)
menu_item.add_url_rule("/menu/<mid>/list", view_func=ListView.as_view("list"))
