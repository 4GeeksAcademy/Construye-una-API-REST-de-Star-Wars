import os
from flask_admin import Admin
from models import db, PrivateData, User, FavoriteElement, Character, Planet, Favorites
from flask_admin.contrib.sqla import ModelView


class UserAdmin(ModelView):
    form_columns = ["user_name", "private_data"]


class FavoriteElementAdmin(ModelView):
    form_columns = ["type"]


class CharacterAdmin(ModelView):
    form_columns = ["id", "name", "age"]


class PlanetAdmin(ModelView):
    form_columns = ["id", "name"]


class FavoritesAdmin(ModelView):

    form_columns = ["user", "element"]



def setup_admin(app):
    app.secret_key = os.environ.get("FLASK_APP_KEY", "sample key")
    app.config["FLASK_ADMIN_SWATCH"] = "cerulean"

    admin = Admin(app, name="4Geeks Admin", template_mode="bootstrap3")

    admin.add_view(ModelView(PrivateData, db.session))
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(FavoriteElementAdmin(FavoriteElement, db.session))
    admin.add_view(CharacterAdmin(Character, db.session))
    admin.add_view(PlanetAdmin(Planet, db.session))
    admin.add_view(FavoritesAdmin(Favorites, db.session))
