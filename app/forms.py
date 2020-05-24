from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    FloatField,
    IntegerField,
)
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Haslo", validators=[DataRequired()])
    submit = SubmitField("Zaloguj")


class RegisterForm(FlaskForm):
    username = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Haslo", validators=[DataRequired()])
    name = StringField("Imie", validators=[DataRequired()])
    last_name = StringField("Nazwisko", validators=[DataRequired()])

    voivodeship = StringField("Województwo", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    street = StringField("Ulica", validators=[DataRequired()])
    building_number = IntegerField("Nr budyku", validators=[DataRequired()])
    house_number = IntegerField("Nr domu", validators=[DataRequired()])

    submit = SubmitField("Zarejestruj")


class ProductForm(FlaskForm):
    name = StringField("Nazwa", validators=[DataRequired()])
    net_price = FloatField("Cena Netto", validators=[DataRequired()])
    vat = FloatField("Vat", validators=[DataRequired()])
    submit = SubmitField("Dodaj Produkt")


class RegisterClientForm(FlaskForm):
    submit = SubmitField("Zarejestruj")
