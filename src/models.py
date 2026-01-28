from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

db = SQLAlchemy()


class PrivateData(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    surname: Mapped[str] = mapped_column(String(120), nullable=False)
    sub_date: Mapped[date] = mapped_column(
        Date, nullable=False, default=date.today)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    user: Mapped["User"] = relationship(
        "User", back_populates="private_data", uselist=False)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False)

    private_data_id: Mapped[int] = mapped_column(
        ForeignKey("private_data.id"), nullable=False)

    private_data: Mapped["PrivateData"] = relationship(
        "PrivateData", back_populates="user", uselist=False)
    favorites: Mapped[list["Favorites"]] = relationship(
        "Favorites", back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "favorites": [f.serialize() for f in self.favorites]
        }


class FavoriteElement(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(
        String(9), nullable=False
    )

    favorites: Mapped[list["Favorites"]] = relationship(
        "Favorites", back_populates="element")
    character: Mapped["Character"] = relationship(
        "Character", back_populates="element", uselist=False)
    planet: Mapped["Planet"] = relationship(
        "Planet", back_populates="element", uselist=False)

    def serialize(self):
        data = {}
        if self.type.lower() == "character" and self.character:
            data = self.character.serialize()
        elif self.type.lower() == "planet" and self.planet:
            data = self.planet.serialize()
        return {
            "id": self.id,
            "type": self.type,
            "details": data
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(ForeignKey(
        "favorite_element.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)

    element: Mapped["FavoriteElement"] = relationship(
        "FavoriteElement", back_populates="character", uselist=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(ForeignKey(
        "favorite_element.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    element: Mapped["FavoriteElement"] = relationship(
        "FavoriteElement", back_populates="planet", uselist=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Favorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    favorite_element_id: Mapped[int] = mapped_column(
        ForeignKey("favorite_element.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="favorites")
    element: Mapped["FavoriteElement"] = relationship(
        "FavoriteElement", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "favorite_element_id": self.element.serialize(),
            "user_id": self.user_id
        }
