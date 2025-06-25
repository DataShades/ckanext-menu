import sqlalchemy as sa
from sqlalchemy.orm import relationship
from typing_extensions import Self
from typing import Any

import ckan.model as model
import ckan.plugins.toolkit as tk
import ckan.types as types

import ckanext.menu.types as menu_types


class CKANMenuModel(tk.BaseModel):
    __tablename__ = "menu"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.Text, nullable=False, unique=True)
    title = sa.Column(sa.Text, nullable=False)
    created = sa.Column(sa.DateTime, server_default=sa.func.now())
    modified = sa.Column(sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())

    items = relationship(
        "CKANMenuItemModel",
        back_populates="menu",
        cascade="all, delete-orphan",
    )

    @classmethod
    def create(cls, data_dict: dict[str, Any]) -> Self:
        menu = cls(**data_dict)

        model.Session.add(menu)
        model.Session.commit()

        return menu

    def delete(self) -> None:
        model.Session().autoflush = False
        model.Session.delete(self)
        model.Session.commit()

    def update(self, data_dict: dict[str, Any]) -> None:
        for key, value in data_dict.items():
            setattr(self, key, value)
        model.Session.commit()

    @classmethod
    def get_by_id(cls, menu_id: str) -> Self | None:
        return model.Session.query(cls).filter(cls.id == menu_id).first()

    @classmethod
    def get_by_name(cls, name: str) -> Self | None:
        return model.Session.query(cls).filter(cls.name == name).first()

    @classmethod
    def get_all(cls) -> list[Self]:
        return model.Session.query(cls).order_by(cls.modified.desc()).all()

    def dictize(self, context: types.Context) -> menu_types.Menu:
        return menu_types.Menu(
            id=str(self.id),
            title=str(self.title),
            name=str(self.name),
            items=[item.dictize(context) for item in self.items],  # type: ignore
            created=self.created.isoformat(),
            modified=self.modified.isoformat(),
        )


class CKANMenuItemModel(tk.BaseModel):
    __tablename__ = "menu_item"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.Text, nullable=False)
    url = sa.Column(sa.String, nullable=False)
    order = sa.Column(sa.Integer, nullable=False, default=0)
    pid = sa.Column(sa.Text, nullable=True)
    classes = sa.Column("classes", sa.String, nullable=True)
    mid = sa.Column(sa.Integer, sa.ForeignKey("menu.id"), nullable=False)

    menu = relationship("CKANMenuModel", back_populates="items")

    @classmethod
    def create(cls, data_dict: dict[str, Any]) -> Self:
        media = cls(**data_dict)

        model.Session.add(media)
        model.Session.commit()

        return media

    def delete(self) -> None:
        model.Session().autoflush = False
        model.Session.delete(self)
        model.Session.commit()

    def update(self, data_dict: dict[str, Any]) -> None:
        for key, value in data_dict.items():
            setattr(self, key, value)
        model.Session.commit()

    @classmethod
    def get_by_id(cls, menu_item_id: str) -> Self | None:
        return model.Session.query(cls).filter(cls.id == menu_item_id).first()

    @classmethod
    def get_by_url(cls, url: str) -> Self | None:
        return model.Session.query(cls).filter(cls.url == url).first()

    @classmethod
    def get_by_menu_id(cls, mid: str) -> list[Self]:
        return model.Session.query(cls).filter(cls.mid == mid).all()

    @classmethod
    def get_menu_items_by_pid(cls, pid: str) -> list[Self]:
        return model.Session.query(cls).filter(cls.pid == pid).all()

    def dictize(self, context: types.Context) -> menu_types.MenuItem:
        return menu_types.MenuItem(
            id=str(self.id),
            title=str(self.title),
            url=str(self.url),
            order=int(self.order),  # type: ignore
            pid=str(self.pid) if self.pid else None,
            classes=str(self.classes) if self.classes else None,
            mid=str(self.mid),
        )
