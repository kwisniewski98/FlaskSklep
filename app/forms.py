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

class DeleteUserForm(FlaskForm):
    submit = SubmitField("Usuń Uzytkownika")
    submitUpdate = SubmitField("Update Uzytkownika")

class DeletePersonForm(FlaskForm):
    submit = SubmitField("Usuń Osobe")
    submitUpdate = SubmitField("Update Osobe")

class DeleteAdresForm(FlaskForm):
    submit = SubmitField("Usuń Adres")
    submitUpdate = SubmitField("Update Adres")

class DeleteProduktForm(FlaskForm):
    submit = SubmitField("Usuń Produkt")
    submitUpdate = SubmitField("Update Produkt")

class UpdateProduktForm(FlaskForm):
    name = StringField("Nazwa", validators=[DataRequired()], default="")
    net_price = FloatField("Cena Netto", validators=[DataRequired()])
    vat = FloatField("Vat", validators=[DataRequired()])
    submit = SubmitField("Update Produkt")

class UpdateAdresForm(FlaskForm):
    voivodeship = StringField("Województwo", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    street = StringField("Ulica", validators=[DataRequired()])
    building_number = IntegerField("Nr budyku", validators=[DataRequired()])
    house_number = IntegerField("Nr domu", validators=[DataRequired()])

    submit = SubmitField("Update Adres")

class UpdateOsobaForm(FlaskForm):
    name = StringField("Imie", validators=[DataRequired()])
    last_name = StringField("Nazwisko", validators=[DataRequired()])
    submit = SubmitField("Update Osoba")


class UpdateUserForm(FlaskForm):
    username = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Haslo", validators=[DataRequired()])
    typ = StringField("Login", validators=[DataRequired()])
    submit = SubmitField("Update Uzytkownika")