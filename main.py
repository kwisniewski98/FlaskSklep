import sqlite3

from flask import Flask, render_template, Config, redirect, _app_ctx_stack, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.forms import LoginForm


DB_NAME = "Database.db"


def create_database(con):
    for file in ["Adres.sql", "Osoba.sql", "Uzytkownik.sql", "Produkt.sql"]:
        with open(f"templates/sql/{file}") as f:
            print(file)
            database = f.read()
            con.execute(database)

def insert_init_values(con):
    inserts = [
        "insert into Adres values(null, 1, 1, 'Dluga', 'Gdansk', 'Pomorskie')",
        "insert into Adres values(null, 2, 2, 'Szeroka', 'Gdansk', 'Pomorskie')",
        "insert into Adres values(null, 3, 3, 'Wojska Polskiego', 'Gdansk', 'Pomorskie')",
        "insert into Osoba values(null, 'Andrzej', 'Kowalski', 1)",
        "insert into Osoba values(null, 'Ania', 'Kowalska', 1)",
        "insert into Osoba values(null, 'Grzegorz', 'Nowak', 2)",
        "insert into Produkt values(null, 'Intel core i7-9700K', 1600, 0.23)",
        "insert into Produkt values(null, 'Intel core i7-9900K', 2200, 0.23)",
        "insert into Uzytkownik values (null, 'temp', 'temp123', 'Manager', 1)",
        "insert into Uzytkownik values (null, 'Klient', 'temp123', 'Klient', 1)",
        "insert into Uzytkownik values (null, 'S', 'temp123', 'Sprzedawca', 1)",
    ]
    for insert in inserts:
        get_db().execute(insert)

def get_db():
    db = getattr(_app_ctx_stack, '_database', None)
    if db is None:
        db = _app_ctx_stack._database = sqlite3.connect(DB_NAME, check_same_thread=False)
    return db


app = Flask(__name__)
app.config.from_object(Config)
con = sqlite3.connect(DB_NAME, check_same_thread=False)
create_database(con)
insert_init_values(con)

app.config.from_object(Config)
secret_key = "cos bezpiecznego"
app.config["SECRET_KEY"] = secret_key
app.secret_key = secret_key



@app.route("/bad_login")
def bad_login():
    return render_template("html/bad_credentials.html.j2", title="Zly Login")


@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        cur = get_db().cursor()
        cur.execute(f"Select haslo from Uzytkownik where login = '{form.username.data}'")
        resp = cur.fetchall()
        print(resp)
        print(form.password.data)
        if resp and cur.fetchall()[0][0] ==form.password.data:
            pass
        else:
            return redirect(url_for("bad_login"))

    return render_template("html/login.html.j2", title="Zaloguj", form=form)


# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(_app_ctx_stack, '_database', None)
#     if db is not None:
#         db.close()


if __name__ == "__main__":
    app.run()
