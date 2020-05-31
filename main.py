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


from app.forms import LoginForm, RegisterForm, RegisterClientForm, ProductForm, DeleteUserForm, DeletePersonForm, DeleteAdresForm, DeleteProduktForm, UpdateProduktForm, UpdateAdresForm, UpdateOsobaForm
from flask import flash

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
        "insert into Produkt values(null, 'Intel core i7-9700K', 1600, 0.23, 1)",
        "insert into Produkt values(null, 'Intel core i7-9900K', 2200, 0.23, 2)",
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
    header = ["Nr", "Nazwa", "Cena netto", "Vat", "Opiekun id"]
    return render_template(
        "html/table.html.j2",
        title="Produkty",
        data=products_list,
        head_values=css,
        header=header,
    )

@app.route("/seller/del_user", methods=["GET", "POST"])
def del_user():

    if session["user_type"] != "Klient":
        form = ProductForm()
        form2 = DeleteUserForm()

        if request.method == "POST":
            cur = get_db().cursor()

            if "Usuń Uzytkownika" == request.form.get("submit"):
                cur.execute('SELECT * FROM Uzytkownik WHERE id=?', (request.form.getlist("przycisk")[0]))
                user = cur.fetchall()[0]
                print((str(user)))
                cur.execute('SELECT * FROM Osoba WHERE id=?', (str(user[0])) )
                person = cur.fetchall()
                cur.execute('SELECT * FROM Adres WHERE id=?', (str(person[0][3])) )
                adress = cur.fetchall()
                if(len(person) == 0):
                    if(len(adress) == 0):
                        cur.execute('DELETE FROM Uzytkownik WHERE id=?', (str(user[0])) )
                        con.commit()
                        flash('Usunieto osobe')
                    else:
                        flash('Musisz najpierw usunac adres', 'error')
                else:
                    flash('Musisz najpierw usunac osobe', 'error')
            
        cur = get_db().cursor()
        cur.execute("Select Osoba.id, imie, nazwisko, login, typ, nr_lokalu, nr_budynku, ulica, miasto, wojewodztwo from Osoba inner join Uzytkownik on Osoba.id = Uzytkownik.id inner join Adres on Adres.id = Osoba.id" )
        return render_template(
            "html/del_user.html.j2", form=form, persons=cur.fetchall(), form2 = form2
        )
    return redirect(url_for("index"))

@app.route("/seller/del_osoba", methods=["GET", "POST"])
def del_osoba():

    if session["user_type"] != "Klient":
        form = DeletePersonForm()

        if request.method == "POST":
            cur = get_db().cursor()

            if "Usuń Osobe" == request.form.get("submit"):
                cur.execute('SELECT * FROM Osoba WHERE id=?', (request.form.getlist("przycisk")[0]) )
                person = cur.fetchall()
                cur.execute('SELECT * FROM Adres WHERE id=?', (str(person[0][3])) )
                adress = cur.fetchall()
                if(len(adress) == 0):
                    cur.execute('DELETE FROM Osoba WHERE id=?', (request.form.getlist("przycisk")[0]) )
                    con.commit()
                    flash('Usunieto osobe')
                else:
                    flash('Musisz najpierw usunac adres', 'error')

            if "Update Osoba" == request.form.get("submitUpdate"):
                print("!!")
                cur = get_db().cursor()
                session["id"] = (request.form.getlist("przycisk"))
                return redirect(url_for("update_osoba"))


        cur = get_db().cursor()
        cur.execute("Select Osoba.id, imie, nazwisko, login, typ, nr_lokalu, nr_budynku, ulica, miasto, wojewodztwo from Osoba inner join Uzytkownik on Osoba.id = Uzytkownik.id inner join Adres on Adres.id = Osoba.id" )
        
        return render_template(
            "html/del_osoba.html.j2", form=form, persons=cur.fetchall()
        )
    return redirect(url_for("index"))

@app.route("/seller/update_osoba", methods=["GET", "POST"])
def update_osoba():

    if session["user_type"] != "Klient":
        form = UpdateOsobaForm()

        if request.method == "POST":
            cur = get_db().cursor()
            if "Update Adres" == request.form.get("submit"):
                con = get_db()
                cur = get_db().cursor()
                ids = str(session['id'])
                #con.execute('update Adres set nazwa=? where id=?',( form.name.data , ids ) )
                #con.execute('update Adres set cena_netto=? where id=?',(form.net_price.data, ids) )
                #con.execute('update Adres set vat=? where id=?',(form.vat.data, ids ) )
                #con.commit()
                return redirect(url_for("index"))

        cur = get_db().cursor()
        cur.execute("Select * from Osoba where id=?",(session["id"]))
        produkty = cur.fetchall()
        form.name.data = produkty[0][1]
        form.surname.data = produkty[0][2]
        
        return render_template(
            "html/update_osoba.html.j2", form=form, persons= produkty
        )
        
    return redirect(url_for("index"))


@app.route("/seller/del_adres", methods=["GET", "POST"])
def del_adres():

    if session["user_type"] != "Klient":
        form = DeleteAdresForm()

        if request.method == "POST":
            cur = get_db().cursor()

            if "Usuń Adres" == request.form.get("submit"):
                cur.execute('SELECT * FROM Adres WHERE id=?', (request.form.getlist("przycisk")[0]) )
                adress = cur.fetchall()
                if(len(adress) == 1):
                    cur.execute('DELETE FROM Adres WHERE id=?', (request.form.getlist("przycisk")[0]) )
                    con.commit()
                    flash('Usunieto Adres')
                else:
                    flash('Nieznany blad', 'error')

            if "Update Adres" == request.form.get("submitUpdate"):
                cur = get_db().cursor()
                session["id"] = (request.form.getlist("przycisk"))
                return redirect(url_for("update_adres"))

        cur = get_db().cursor()
        cur.execute("Select id, nr_lokalu, nr_budynku, ulica, miasto, wojewodztwo from Adres")
        return render_template(
            "html/del_adres.html.j2", form=form, persons=cur.fetchall()
        )
    return redirect(url_for("index"))

@app.route("/seller/update_adres", methods=["GET", "POST"])
def update_adres():

    if session["user_type"] != "Klient":
        form = UpdateAdresForm()

        if request.method == "POST":
            cur = get_db().cursor()
            if "Update Adres" == request.form.get("submit"):
                con = get_db()
                cur = get_db().cursor()
                ids = str(session['id'])
                #con.execute('update Adres set nazwa=? where id=?',( form.name.data , ids ) )
                #con.execute('update Adres set cena_netto=? where id=?',(form.net_price.data, ids) )
                #con.execute('update Adres set vat=? where id=?',(form.vat.data, ids ) )
                #con.commit()
                return redirect(url_for("index"))

        cur = get_db().cursor()
        cur.execute("Select * from Adres where id=?",(session["id"]))
        produkty = cur.fetchall()
        form.building_number.data = produkty[0][1]
        form.house_number.data = produkty[0][2]
        form.street.data = produkty[0][3]
        form.city.data = produkty[0][4]
        form.voivodeship.data = produkty[0][5]
        
        return render_template(
            "html/update_adres.html.j2", form=form, persons= produkty
        )
        
    return redirect(url_for("index"))

@app.route("/seller/del_produkt", methods=["GET", "POST"])
def del_produkt():

    if session["user_type"] != "Klient":
        form = DeleteProduktForm()

        if request.method == "POST":
            cur = get_db().cursor()

            if "Usuń Produkt" == request.form.get("submit"):
                cur.execute('SELECT * FROM Produkt WHERE id=?', (request.form.getlist("przycisk")[0]) )
                produkt = cur.fetchall()
                if(len(produkt) == 1):
                    cur.execute('DELETE FROM Produkt WHERE id=?', (request.form.getlist("przycisk")[0]) )
                    con.commit()
                    flash('Usunieto Produkt')
                else:
                    flash('Nieznany blad', 'error')

            if "Update Produkt" == request.form.get("submitUpdate"):
                cur = get_db().cursor()
                session["id"] = (request.form.getlist("przycisk"))
                return redirect(url_for("update_product"))

        cur = get_db().cursor()
        cur.execute("Select id, nazwa, cena_netto, vat, opiekun from Produkt")
        return render_template(
            "html/del_produkt.html.j2", form=form, persons=cur.fetchall()
        )
    return redirect(url_for("index"))


@app.route("/seller/update_product", methods=["GET", "POST"])
def update_product():

    if session["user_type"] != "Klient":
        form = UpdateProduktForm()

        if request.method == "POST":
            cur = get_db().cursor()
            if "Update Produkt" == request.form.get("submit"):
                con = get_db()
                cur = get_db().cursor()
                ids = str(session['id'])
                con.execute('update Produkt set nazwa=? where id=?',( form.name.data , ids ) )
                con.execute('update Produkt set cena_netto=? where id=?',(form.net_price.data, ids) )
                con.execute('update Produkt set vat=? where id=?',(form.vat.data, ids ) )
                con.commit()
                return redirect(url_for("index"))

        cur = get_db().cursor()
        cur.execute("Select id, nazwa, cena_netto, vat, opiekun from Produkt where id=?",(session["id"]))
        produkty = cur.fetchall()
        form.name.data = produkty[0][1]
        form.net_price.data = produkty[0][2]
        form.vat.data = produkty[0][3]
        
        return render_template(
            "html/update_product.html.j2", form=form, persons= produkty
        )
        
    return redirect(url_for("index"))



@app.route("/seller/add_product", methods=["GET", "POST"])
def add_product():
    
    if session["user_type"] != "Klient":
        form = ProductForm()
        form2 = DeleteUserForm()
        if request.method == "POST":
            cur = get_db().cursor()
            form.validate_on_submit()
            cur.execute(
                "insert into Produkt values (null, ?, ?, ?, ?)",
                (
                    form.name.data,
                    form.net_price.data,
                    form.vat.data,
                    request.getlist("przycisk")[0],
                ),
            )
            get_db().commit()
            return redirect(url_for("products"))
        cur = get_db().cursor()
        cur.execute("Select id, imie, nazwisko from Osoba")
        return render_template(
            "html/add_product.html.j2", form=form, persons=cur.fetchall(), form2 = form2
        )
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
        if session["register_type"] == "Klient":
            return redirect(url_for("login"))
        else:
            return redirect(url_for("index"))

    return render_template("html/register.html.j2", title="Zarejestruj", form=form)


@app.route("/index.html", methods=["GET", "POST"])
def index():
    if request.method =="GET":
        if "user_type" not in session.keys():
            return redirect(url_for("bad_login"))
        css = """<style type="text/css">
    form input[type="submit"]{
    
        background: none;
        border: none;
        color: blue;
        text-decoration: underline;
        cursor: pointer;
    }
    </style>"""
        return render_template(
            "html/index.html.j2",
            title="Główna",
            user_type=session["user_type"],
            head_values=css,
        )
    else:
        if request.form.get("submit") == "Zarejestruj Sprzedawce":
            session["register_type"] = "Sprzedawca"
            return redirect(url_for("register"))
        elif request.form.get("submit") == "Zarejestruj Managera":
            session["register_type"] = "Manager"
            return redirect(url_for("register"))

        elif request.form.get("submit") == "Usuń Użytkownika":
            session["register_type"] = "Sprzedawca"
            return redirect(url_for("del_user"))

        elif request.form.get("submit") == "Usuń Osobe":
            session["register_type"] = "Sprzedawca"
            return redirect(url_for("del_osoba"))
            
        elif request.form.get("submit") == "Usuń Adres":
            session["register_type"] = "Sprzedawca"
            return redirect(url_for("del_adres"))
        elif request.form.get("submit") == "Usuń Produkt":
            session["register_type"] = "Sprzedawca"
            return redirect(url_for("del_produkt"))
if __name__ == "__main__":
    app.run()
