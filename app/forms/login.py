from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Required, EqualTo, Email, ValidationError
from app.models.users import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        Required('Email field is required'),
        Email()
    ])
    password = PasswordField('Password', validators=[
        Required("Password field is required")
    ])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    first_name = StringField("First name", validators=[
        Required("First name is required")
    ])
    last_name = StringField("Last name", validators=[
        Required("Last name is required")
    ])
    email = StringField('Email', validators=[
        Required('Email field is required'),
        Email()
    ])
    password = PasswordField('Password', validators=[
        Required("Password field is required")
    ])
    password2 = PasswordField('Confirm password', validators=[
        Required("Confirm password field is required"),
        EqualTo("password", message="Passwords must match")
    ])

    def validate_email(self, email: str):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Email already registered.")
        return


def flash_form_errors(form: FlaskForm) -> None:
    """Flash messages for forms' errors/

    Args:
        form (FlaskForm): FlaskForm having errors
    """
    for field, errors in form.errors.items():
        for error in errors:
            flash("Error in the {} field - {}".format(
                getattr(form, field).label.text,
                error
            ))
    return
