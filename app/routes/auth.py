from app import app, db, login_manager
from app.models.users import User
from flask import Blueprint
from flask import render_template, request, redirect, flash, url_for
from werkzeug.urls import url_parse
from app.forms.login import LoginForm, RegistrationForm, flash_form_errors
from flask_login import current_user, login_user, login_required, logout_user


auth = Blueprint("auth", __name__, template_folder="../templates/auth/")


@login_required
@auth.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm(request.form)
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=request.form["email"]).first()
        if user is None or not user.check_password(request.form["password"]):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        remember_me = False
        if "remember_me" in request.form:
            remember_me = True
        login_user(user, remember=remember_me)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    flash_form_errors(login_form)
    return render_template(
        "login.html",
        page_title="Log in",
        form=login_form
    )


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@auth.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User.create_user(
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            email=request.form["email"],
            password=request.form["password"]

        )
        if user is not None:
            flash("Successfully registered.")
            return redirect(url_for("index"))
        else:
            flash("Error registering user. Please try again")
            return redirect(url_for("index"))
    flash_form_errors(form)
    return render_template("register.html", form=form, page_title="Register")


login_manager.login_view = "auth.login"