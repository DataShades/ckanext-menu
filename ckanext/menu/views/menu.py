from __future__ import annotations

from flask import Blueprint
from flask.views import MethodView
from sqlalchemy import or_


import ckan.lib.navl.dictization_functions as dict_fns
import ckan.logic as logic
import ckan.plugins.toolkit as tk
from ckan.types import Context
import ckan.model as model
from ckan.lib.helpers import Page, pager_url

from ckanext.menu.model.menu import CKANMenuModel


ValidationError = logic.ValidationError

menu = Blueprint("menu", __name__)


def make_context() -> Context:
    return {
        "user": tk.current_user.name,
        "auth_user_obj": tk.current_user,
    }


class CreateView(MethodView):
    def get(self):
        try:
            tk.check_access("menu_create", make_context(), {})
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

        extra_vars = {
            "form_data": form_data,
            "errors": {},
        }

        return tk.render("menu/create.html", extra_vars=extra_vars)

    def post(self):
        try:
            tk.check_access("menu_create", make_context(), {})
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

        try:
            tk.get_action("menu_create")(make_context(), form_data)
        except logic.ValidationError as e:
            tk.h.flash_error(e.error_summary)
            return tk.render(
                "menu/create.html",
                extra_vars={"form_data": form_data, "errors": {}},
            )

        return tk.redirect_to("menu.list")


class EditView(MethodView):
    def get(self, id: str):
        menu = CKANMenuModel.get_by_id(id)

        try:
            tk.check_access("menu_edit", make_context(), {"id": id})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        if not menu:
            return tk.abort(404, "Page not found")

        form_data = menu.dictize({})

        return tk.render(
            "menu/edit.html",
            extra_vars={
                "id": id,
                "form_data": form_data,
                "errors": {},
            },
        )

    def post(self, id: str):
        try:
            tk.check_access("menu_edit", make_context(), {})
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

        try:
            tk.get_action("menu_edit")(make_context(), form_data)
        except logic.ValidationError as e:
            tk.h.flash_error(e.error_summary)
            return tk.render(
                "menu/edit.html",
                extra_vars={"form_data": form_data, "errors": {}},
            )

        return tk.redirect_to("menu.list")


class DeleteView(MethodView):
    def get(self, id: str):
        menu = CKANMenuModel.get_by_id(id)

        try:
            tk.check_access("menu_delete", make_context(), {"id": id})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        if not menu:
            return tk.abort(404, "Page not found")

        form_data = menu.dictize({})

        return tk.render(
            "menu/delete.html",
            extra_vars={
                "id": id,
                "form_data": form_data,
                "errors": {},
            },
        )

    def post(self, id: str):
        try:
            tk.check_access("menu_delete", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        form_data = {"id": id}

        try:
            tk.get_action("menu_delete")(make_context(), form_data)
        except logic.ValidationError as e:
            tk.h.flash_error(e.error_summary)
            return tk.render(
                "menu/delete.html",
                extra_vars={"form_data": form_data, "errors": {}},
            )

        return tk.redirect_to("menu.list")


class ReadView(MethodView):
    def _check_access(self, id: str):
        try:
            tk.check_access("menu_view", make_context(), {"id": id})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

    def get(self, id: str):
        menu = CKANMenuModel.get_by_id(id)

        if not menu:
            return tk.abort(404, "Page not found")

        self._check_access(id)

        return tk.render(
            "menu/read.html",
            extra_vars={
                "id": id,
                "menu": menu.dictize({}),
            },
        )


class ListView(MethodView):
    def get(self):
        try:
            tk.check_access("menu_create", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        extra_vars = {}
        extra_vars["q"] = q = tk.request.args.get("q", "")
        page = tk.h.get_page_number(tk.request.args)
        limit = 20

        query = model.Session.query(CKANMenuModel)

        if q:
            query = query.filter(
                or_(
                    CKANMenuModel.title.ilike("%" + q.strip() + "%"),
                    CKANMenuModel.name.ilike("%" + q.strip() + "%"),
                )
            )

        extra_vars["count"] = count = query.count()

        query = (
            query.order_by(CKANMenuModel.modified.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        menus = [item.dictize({}) for item in query]

        extra_vars["page"] = Page(
            collection=menus,
            page=page,
            url=pager_url,
            item_count=count,
            items_per_page=limit,
        )
        extra_vars["page"].items = menus

        return tk.render("menu/list.html", extra_vars=extra_vars)


menu.add_url_rule("/menu/list", view_func=ListView.as_view("list"))
menu.add_url_rule("/menu/create", view_func=CreateView.as_view("create"))
menu.add_url_rule("/menu/edit/<id>", view_func=EditView.as_view("edit"))
menu.add_url_rule("/menu/delete/<id>", view_func=DeleteView.as_view("delete"))
menu.add_url_rule("/menu/<id>", view_func=ReadView.as_view("read"))
