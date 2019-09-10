from app import app, db, login_manager
from ..models.users import User
from flask import Blueprint, render_template
from flask_login import current_user, login_required

admin = Blueprint(
    "admin", __name__, template_folder="../templates/admin",
    url_prefix="/admin"
)


@login_required
@admin.route("/users")
def view_all_users():
    if current_user.is_admin():
        return render_template("users.html", page_title="All users")