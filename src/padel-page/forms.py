from random import choices

from flask_wtf import FlaskForm
from models import User
from wtforms import (
    BooleanField,
    DateField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
    TimeField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=32)]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=64)]
    )
    password2 = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class GameForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    start_time = TimeField("Start time", validators=[DataRequired()])
    end_time = TimeField("End time", validators=[DataRequired()])
    arena = SelectField("Arena")
    league = SelectField("League")
    players = SelectMultipleField("Players", validate_choice=False)

    submit = SubmitField("Add")

    def validate_players(self, players):
        if not len(players.data) == 4:
            raise ValidationError("Please select 4 players")


class StatForm(FlaskForm):
    winners = SelectMultipleField("Winners", validate_choice=False)
    losers = SelectMultipleField("Losers", validate_choice=False)

    submit = SubmitField("Add statistics!")

    def validate_winners(self, winners):
        if not len(winners.data) == 2:
            raise ValidationError("It should be two winners!")

    def validate_losers(self, losers):
        if not len(losers.data) == 2:
            raise ValidationError("It should be two losers")
