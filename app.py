from flask import Flask
import sqlite3
import secrets
from flask import abort, redirect, render_template, request, session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import db
import config

app = Flask(__name__)
app.secret_key = config.secret_key

categories = [
    "Kotityöt",
    "Puutarha/Pihatyöt",
    "Kuljetus",
    "Kantaminen",
    "Muu"
]

def require_login():
    if "user_id" not in session:
        return False
    return True

def check_csrf():
    if request.form.get("csrf_token") != session.get("csrf_token"):
        abort(403)

def get_item(item_id):
    sql = """
        SELECT items.id,
               items.title,
               items.description,
               items.reward,
               items.location,
               items.category,
               items.created_at,
               items.user_id,
               users.username
        FROM items, users
        WHERE items.user_id = users.id AND items.id = ?
    """
    result = db.query(sql, [item_id])

    if len(result) == 0:
        return None

    return result[0]

def get_user(user_id):
    sql = """
        SELECT id, username, created_at
        FROM users
        WHERE id = ?
    """
    result = db.query(sql, [user_id])

    if len(result) == 0:
        return None

    return result[0]

@app.route("/")
def index():
    query = request.args.get("q", "").strip()

    if query:
        like = "%" + query + "%"
        sql = """
            SELECT items.id,
                   items.title,
                   items.description,
                   items.reward,
                   items.location,
                   items.category,
                   items.created_at,
                   items.user_id,
                   users.username
            FROM items, users
            WHERE items.user_id = users.id
              AND (items.title LIKE ? OR items.description LIKE ? OR items.location LIKE ?)
            ORDER BY items.id DESC
        """
        items = db.query(sql, [like, like, like])
    else:
        sql = """
            SELECT items.id,
                   items.title,
                   items.description,
                   items.reward,
                   items.location,
                   items.category,
                   items.created_at,
                   items.user_id,
                   users.username
            FROM items, users
            WHERE items.user_id = users.id
            ORDER BY items.id DESC
        """
        items = db.query(sql)

    return render_template("index.html", items=items, query=query)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"].strip()
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if not username:
        return render_template("register.html", error="Tunnus puuttuu", username=username)

    if password1 != password2:
        return render_template("register.html", error="Salasanat eivät ole samat", username=username)

    if len(password1) < 4:
        return render_template("register.html", error="Salasanan pitää olla vähintään 4 merkkiä pitkä", username=username)

    password_hash = generate_password_hash(password1, method="pbkdf2:sha256")

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return render_template("register.html", error="Tunnus on jo varattu", username=username)

    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])

        if len(result) == 0:
            return render_template("login.html", error="Väärä tunnus tai salasana", username=username)

        user = result[0]
        password_hash = user["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user["id"]
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            return render_template("login.html", error="Väärä tunnus tai salasana", username=username)

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]

    if "username" in session:
        del session["username"]

    if "csrf_token" in session:
        del session["csrf_token"]

    return redirect("/")

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = get_user(user_id)

    if not user:
        return "VIRHE: käyttäjää ei löytynyt"

    sql = """
        SELECT items.id,
               items.title,
               items.description,
               items.reward,
               items.location,
               items.category,
               items.created_at,
               items.user_id
        FROM items
        WHERE items.user_id = ?
        ORDER BY items.id DESC
    """
    items = db.query(sql, [user_id])

    return render_template("user.html", user=user, items=items)

@app.route("/new_item")
def new_item():
    if not require_login():
        return redirect("/login")

    return render_template("new_item.html", categories=categories)

@app.route("/create_item", methods=["POST"])
def create_item():
    if not require_login():
        return redirect("/login")

    check_csrf()

    title = request.form["title"].strip()
    description = request.form["description"].strip()
    reward = request.form["reward"].strip()
    location = request.form["location"].strip()
    category = request.form["category"]

    form = {
        "title": title,
        "description": description,
        "reward": reward,
        "location": location,
        "category": category
    }

    if not title:
        return render_template("new_item.html", categories=categories, error="Otsikko puuttuu", form=form)

    if not description:
        return render_template("new_item.html", categories=categories, error="Kuvaus puuttuu", form=form)

    if not reward:
        return render_template("new_item.html", categories=categories, error="Palkkio puuttuu", form=form)

    if category not in categories:
        return render_template("new_item.html", categories=categories, error="Virheellinen luokitus", form=form)

    try:
        reward_value = int(reward)
    except ValueError:
        return render_template("new_item.html", categories=categories, error="Palkkion pitää olla kokonaisluku", form=form)

    if reward_value < 0:
        return render_template("new_item.html", categories=categories, error="Palkkio ei voi olla negatiivinen", form=form)

    sql = """
        INSERT INTO items (title, description, reward, location, category, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    db.execute(sql, [title, description, reward_value, location, category, session["user_id"]])

    return redirect("/")

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = get_item(item_id)

    if not item:
        return "VIRHE: ilmoitusta ei löytynyt"

    return render_template("show_item.html", item=item)

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    if not require_login():
        return redirect("/login")

    item = get_item(item_id)

    if not item:
        return "VIRHE: ilmoitusta ei löytynyt"

    if item["user_id"] != session["user_id"]:
        return "VIRHE: ei oikeutta muokata tätä ilmoitusta"

    return render_template("edit_item.html", item=item, categories=categories)

@app.route("/update_item/<int:item_id>", methods=["POST"])
def update_item(item_id):
    if not require_login():
        return redirect("/login")

    check_csrf()

    item = get_item(item_id)

    if not item:
        return "VIRHE: ilmoitusta ei löytynyt"

    if item["user_id"] != session["user_id"]:
        return "VIRHE: ei oikeutta muokata tätä ilmoitusta"

    title = request.form["title"].strip()
    description = request.form["description"].strip()
    reward = request.form["reward"].strip()
    location = request.form["location"].strip()
    category = request.form["category"]

    form = {
        "id": item_id,
        "title": title,
        "description": description,
        "reward": reward,
        "location": location,
        "category": category
    }

    if not title:
        return render_template("edit_item.html", item=form, categories=categories, error="Otsikko puuttuu")

    if not description:
        return render_template("edit_item.html", item=form, categories=categories, error="Kuvaus puuttuu")

    if not reward:
        return render_template("edit_item.html", item=form, categories=categories, error="Palkkio puuttuu")

    if category not in categories:
        return render_template("edit_item.html", item=form, categories=categories, error="Virheellinen luokitus")

    try:
        reward_value = int(reward)
    except ValueError:
        return render_template("edit_item.html", item=form, categories=categories, error="Palkkion pitää olla kokonaisluku")

    if reward_value < 0:
        return render_template("edit_item.html", item=form, categories=categories, error="Palkkio ei voi olla negatiivinen")

    sql = """
        UPDATE items
        SET title = ?, description = ?, reward = ?, location = ?, category = ?
        WHERE id = ?
    """
    db.execute(sql, [title, description, reward_value, location, category, item_id])

    return redirect("/item/" + str(item_id))

@app.route("/delete_item/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    if not require_login():
        return redirect("/login")

    check_csrf()

    item = get_item(item_id)

    if not item:
        return "VIRHE: ilmoitusta ei löytynyt"

    if item["user_id"] != session["user_id"]:
        return "VIRHE: ei oikeutta poistaa tätä ilmoitusta"

    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

    return redirect("/")