from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Haslo', validators=[DataRequired()])
    submit = SubmitField('Zaloguj')


class RegisterForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Haslo', validators=[DataRequired()])
    voivodeship = PasswordField('Województwo', validators=[DataRequired()])
    city = PasswordField('City', validators=[DataRequired()])
    street = PasswordField('Ulica', validators=[DataRequired()])
    building_number = PasswordField('Nr budyku', validators=[DataRequired()])
    house_number = PasswordField('Nr domu', validators=[DataRequired()])

    submit = SubmitField('Zarejestruj')

class RegisterClientForm(FlaskForm):
    submit = SubmitField("Zarejestruj")