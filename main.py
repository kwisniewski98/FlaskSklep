import json
import sqlite3

from flask import (
    Flask,
    render_template,
    Config,
    redirect,
    _app_ctx_stack,
    url_for,
    session,
    request,
)


from app.forms import LoginForm, RegisterForm, RegisterClientForm, ProductForm

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
        con.execute(insert)
    con.commit()


def get_db():
    db = getattr(_app_ctx_stack, "_database", None)
    if db is None:
        db = _app_ctx_stack._database = sqlite3.connect(
            DB_NAME, check_same_thread=False
        )
    return db


app = Flask(__name__)
app.config.from_object(Config)
con = sqlite3.connect(DB_NAME, check_same_thread=False)
create_database(con)
# insert_init_values(con)

app.config.from_object(Config)
secret_key = "cos bezpiecznego"
app.config["SECRET_KEY"] = secret_key
app.secret_key = secret_key


@app.route("/bad_login")
def bad_login():
    return render_template("html/bad_credentials.html.j2", title="Zly Login")


@app.route("/", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    register_form = RegisterClientForm()

    if request.method == "POST":

        if "Zaloguj" == request.form.get("submit"):
            cur = get_db().cursor()
            cur.execute(
                f"Select haslo, typ from Uzytkownik where login = '{login_form.username.data}'"
            )
            resp = cur.fetchall()

            if resp and resp[0][0] == login_form.password.data:
                session["user_type"] = resp[0][1]
                return redirect(url_for("index"))
            else:
                return redirect(url_for("bad_login"))
        elif "Zarejestruj" == request.form.get("submit"):
            session["register_type"] = "Klient"
            return redirect(url_for("register"))
        else:
            return redirect(url_for("login"))

    return render_template(
        "html/login.html.j2", title="Zaloguj", form=login_form, form2=register_form
    )


@app.route("/client/products")
def products():
    con = get_db()
    cur = con.cursor()
    cur.execute("Select * from Produkt")
    products_list = cur.fetchall()
    css = """
    <style>
table {
  border-collapse: collapse;
}

table, th, td {
  border: 1px solid black;
}
    </style>"""
    header = ["Nr", "Nazwa", "Cena netto", "Vat"]
    return render_template(
        "html/table.html.j2",
        title="Produkty",
        data=products_list,
        head_values=css,
        header=header,
    )


# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(_app_ctx_stack, '_database', None)
#     if db is not None:
#         db.close()
@app.route("/seller/add_product", methods=["GET", "POST"])
def add_product():
    if session["user_type"] != "Klient":
        form = ProductForm()
        if request.method == "POST":
            form.validate_on_submit()
            cur = get_db().cursor()
            cur.execute(
                "insert into Produkt values (null, ?, ?, ?)",
                (form.name.data, form.net_price.data, form.vat.data),
            )
            get_db().commit()
            return redirect(url_for("products"))

        return render_template("html/add_product.html.j2", form=form)
    return redirect(url_for("index"))


@app.route("/manager/users")
def users():
    if session["user_type"] != "Klient":
        cur = get_db().cursor()
        cur.execute(
            "select login, haslo, typ, imie, nazwisko, wojewodztwo, miasto, ulica,"
            " nr_budynku, nr_lokalu from Uzytkownik "
            "inner join Osoba on Uzytkownik.osoba = Osoba.id"
            " inner join Adres on Osoba.adres = Adres.id "
        )
        resp = cur.fetchall()
        css = """
            <style>
        table {
          border-collapse: collapse;
        }

        table, th, td {
          border: 1px solid black;
        }
            </style>"""
        header = [
            "Login",
            "Hasło",
            "Typ",
            "Imie",
            "Nazwisko",
            "Województwo",
            "Miasto",
            "Ulica",
            "Nr Budynku",
            "Nr lokalu",
        ]
        return render_template(
            "html/table.html.j2", data=resp, head_values=css, header=header
        )
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        form.validate_on_submit()
        cur = get_db().cursor()
        cur.execute(
            "insert into Adres values (null, ?, ?, ?, ?, ?)",
            (
                form.house_number.data,
                form.building_number.data,
                form.street.data,
                form.city.data,
                form.voivodeship.data,
            ),
        )
        get_db().commit()
        addres_id = cur.lastrowid
        cur.execute(
            "insert into Osoba values (null, ?, ?, ?)",
            (form.name.data, form.last_name.data, addres_id),
        )
        get_db().commit()
        user_id = cur.lastrowid
        cur.execute(
            "insert into Uzytkownik values (null, ?, ?, ?, ?)",
            (form.username.data, form.password.data, session["register_type"], user_id),
        )
        get_db().commit()
        return redirect(url_for("login"))

    return render_template("html/register.html.j2", title="Zarejestruj", form=form)


@app.route("/index.html")
def index():
    if "user_type" not in session.keys():
        return redirect(url_for("bad_login"))
    return render_template(
        "html/index.html.j2", title="Główna", user_type=session["user_type"]
    )


if __name__ == "__main__":
    app.run()
