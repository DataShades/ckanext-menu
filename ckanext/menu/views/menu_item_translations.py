from __future__ import annotations

from flask import Blueprint
from flask.views import MethodView


import ckan.lib.navl.dictization_functions as dict_fns
import ckan.logic as logic
import ckan.plugins.toolkit as tk
from ckan.types import Context

from ckanext.menu.model.menu import CKANMenuItemModel


ValidationError = logic.ValidationError

menu_item_translations = Blueprint("menu_item_translations", __name__)


def make_context() -> Context:
    return {
        "user": tk.current_user.name,
        "auth_user_obj": tk.current_user,
    }


class CreateTranslationView(MethodView):
    def get(self, mid: int, id: int, lang: str):
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

        menu_item = CKANMenuItemModel.get_by_id(id)

        if not menu_item:
            return tk.abort(404, "Page not found")

        form_data['title'] = form_data['title'] if form_data.get(
            'title') else menu_item.title

        extra_vars = {
            "mid": mid,
            "menu_item": menu_item,
            "form_data": form_data,
            "errors": {},
            "id": id,
            "lang": lang,
        }

        return tk.render("menu/menu_item/translations/create.html", extra_vars=extra_vars)

    def post(self, mid: int, id: int, lang: str):
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

        form_data["id"] = id
        form_data["lang"] = lang

        try:
            tk.get_action("menu_item_create_translation")(
                make_context(), form_data)
        except logic.ValidationError as e:
            tk.h.flash_error(e.error_summary)

            return tk.render(
                "menu/menu_item/translations/create.html",
                extra_vars=form_data,
            )

        return tk.redirect_to("menu_item_translations.list", mid=mid, id=id)


class TranslationEditView(MethodView):
    def get(self, mid: int, id: int, lang: str):
        menu_item = CKANMenuItemModel.get_by_id(id)

        try:
            tk.check_access("menu_edit", make_context(), {"id": id})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        if not menu_item:
            return tk.abort(404, "Page not found")

        translations = menu_item.translations

        if not translations or not translations.get(lang):
            return tk.abort(404, "Page not found")

        data = translations[lang]

        extra_vars = {
            "id": id,
            "mid": mid,
            "form_data": data,
            "errors": {},
            "lang": lang,
        }

        return tk.render(
            "menu/menu_item/translations/edit.html",
            extra_vars=extra_vars,
        )

    def post(self, mid: int, id: int, lang: str):
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
        form_data["lang"] = lang

        try:
            tk.get_action("menu_item_create_translation")(
                make_context(), form_data)
        except logic.ValidationError as e:
            tk.h.flash_error(e.error_summary)
            extra_vars = {
                "id": id,
                "mid": mid,
                "form_data": form_data,
                "errors": {},
                "lang": lang,
            }

            return tk.render(
                "menu/menu_item/translations/edit.html",
                extra_vars=extra_vars,
            )

        return tk.redirect_to("menu_item_translations.list", mid=mid, id=id)


class TranslationsView(MethodView):
    def get(self, mid: int, id: int):
        try:
            tk.check_access("menu_item_create", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        menu_item = CKANMenuItemModel.get_by_id(id)

        extra_vars = {
            "menu_item": menu_item,
            "mid": mid,
            "id": id,
        }

        return tk.render("menu/menu_item/translations/list.html", extra_vars=extra_vars)


class TranslationDeleteView(MethodView):
    def get(self, mid: int, id: int, lang: str):
        menu_item = CKANMenuItemModel.get_by_id(id)

        try:
            tk.check_access("menu_item_delete", make_context(), {"id": id})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        if not menu_item:
            return tk.abort(404, "Page not found")

        form_data = menu_item.dictize({})

        return tk.render(
            "menu/menu_item/translations/delete.html",
            extra_vars={
                "id": id,
                "form_data": form_data,
                "errors": {},
                "mid": mid,
                "lang": lang
            },
        )

    def post(self, mid: int, id: int, lang: str):
        try:
            tk.check_access("menu_item_delete", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        form_data = {"id": id, "lang": lang}

        extra_vars = {
            "id": id,
            "form_data": form_data,
            "errors": {},
            "mid": mid,
            "lang": lang
        },

        try:
            tk.get_action("menu_item_delete_translation")(
                make_context(), form_data)
        except logic.ValidationError as e:
            tk.h.flash_error(e.error_summary)
            return tk.render(
                "menu/menu_item/translations/delete.html",
                extra_vars=extra_vars,
            )

        return tk.redirect_to("menu_item_translations.list", mid=mid, id=id)


menu_item_translations.add_url_rule(
    "/menu/<mid>/menu-item/<id>/translation/<lang>/create", view_func=CreateTranslationView.as_view("create")
)
menu_item_translations.add_url_rule(
    "/menu/<mid>/menu-item/<id>/translation/<lang>/edit", view_func=TranslationEditView.as_view("edit")
)
menu_item_translations.add_url_rule(
    "/menu/<mid>/menu-item/<id>/translation/<lang>/delete", view_func=TranslationDeleteView.as_view("delete")
)
menu_item_translations.add_url_rule(
    "/menu/<mid>/menu-item/<id>/translations", view_func=TranslationsView.as_view("list"))
