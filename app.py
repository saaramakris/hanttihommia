import secrets
import sqlite3

from flask import Flask, abort, redirect, render_template, request, session

import config
import items
import messages as message_queries
import users

app = Flask(__name__)
app.secret_key = config.secret_key

categories = [
 "Kotityöt",
 "Puutarha/Pihatyöt",
 "Kuljetus",
 "Kantaminen",
 "Muu"
]

MAX_USERNAME_LENGTH = 30
MAX_TITLE_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 5000
MAX_LOCATION_LENGTH = 100
MAX_MESSAGE_LENGTH = 5000

def require_login():
 if "user_id" not in session:
  return False
 return True

def check_csrf():
 if request.form.get("csrf_token") != session.get("csrf_token"):
  abort(403)

@app.route("/")
def index():
 query = request.args.get("q", "").strip()
 location = request.args.get("location", "").strip()
 category = request.args.get("category", "").strip()
 if query or location or category:
  all_items = items.search_items(query, location, category)
 else:
  all_items = items.get_items()
 return render_template(
  "index.html",
  items=all_items,
  query=query,
  location=location,
  category=category,
  categories=categories
 )

@app.route("/register")
def register():
 return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
 username = request.form["username"].strip()
 password1 = request.form["password1"]
 password2 = request.form["password2"]
 if not username:
  return render_template(
   "register.html",
   error="Tunnus puuttuu",
   username=username
  )
 
 if len(username) > MAX_USERNAME_LENGTH:
  return render_template(
   "register.html",
   error="Tunnus on liian pitkä",
   username=username
  )
 
 if password1 != password2:
  return render_template(
   "register.html",
   error="Salasanat eivät ole samat",
   username=username
  )
 
 if len(password1) < 4:
  return render_template(
   "register.html",
   error="Salasanan pitää olla vähintään 4 merkkiä pitkä",
   username=username
  )
 
 try:
  users.create_user(username, password1)
 except sqlite3.IntegrityError:
  return render_template(
   "register.html",
   error="Tunnus on jo varattu",
   username=username
  )
 return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
 if request.method == "GET":
  return render_template("login.html")
 username = request.form["username"].strip()
 password = request.form["password"]
 user = users.check_login(username, password)
 if user:
  session["user_id"] = user["id"]
  session["username"] = username
  session["csrf_token"] = secrets.token_hex(16)
  return redirect("/")
 return render_template(
  "login.html",
  error="Väärä tunnus tai salasana",
  username=username
 )

@app.route("/logout")
def logout():
 if "user_id" in session:
  del session["user_id"]
 if "username" in session:
  del session["username"]
 if "csrf_token" in session:
  del session["csrf_token"]
 return redirect("/")

@app.route("/messages")
def messages():
 if not require_login():
  return redirect("/login")
 user_messages = message_queries.get_messages(session["user_id"])
 return render_template("messages.html", messages=user_messages)

@app.route("/messages/<int:thread_id>")
def show_message_thread(thread_id):
 if not require_login():
  return redirect("/login")
 thread = message_queries.get_thread(thread_id, session["user_id"])
 if len(thread) == 0:
  return "VIRHE: viestiketjua ei löytynyt tai sinulla ei ole oikeutta nähdä sitä"
 return render_template("message_thread.html", messages=thread)

@app.route("/messages/<int:thread_id>/reply", methods=["POST"])
def reply_message(thread_id):
 if not require_login():
  return redirect("/login")
 check_csrf()
 content = request.form["content"].strip()
 thread = message_queries.get_thread(thread_id, session["user_id"])
 if len(thread) == 0:
  return "VIRHE: viestiketjua ei löytynyt tai sinulla ei ole oikeutta nähdä sitä"
 first_message = thread[0]
 if session["user_id"] == first_message["sender_id"]:
  receiver_id = first_message["receiver_id"]
 else:
  receiver_id = first_message["sender_id"]
 if not content:
  return render_template(
   "message_thread.html",
   messages=thread,
   error="Vastaus puuttuu"
  )
 
 if len(content) > MAX_MESSAGE_LENGTH:
  return render_template(
   "message_thread.html",
   messages=thread,
   error="Vastaus on liian pitkä"
  )
 
 message_queries.add_reply(
  thread_id,
  session["user_id"],
  receiver_id,
  first_message["item_id"],
  content
 )
 return redirect("/messages/" + str(thread_id))

@app.route("/message_item/<int:item_id>")
def message_item(item_id):
 if not require_login():
  return redirect("/login")
 item = items.get_item(item_id)
 if not item:
  user_messages = message_queries.get_messages(session["user_id"])
  return render_template(
   "messages.html",
   messages=user_messages,
   error="Ilmoitusta ei löydy tai se on poistettu"
  )
 return redirect("/item/" + str(item_id))

@app.route("/contact/<int:item_id>")
def contact(item_id):
 if not require_login():
  return redirect("/login")
 item = items.get_item(item_id)
 if not item:
  return "VIRHE: ilmoitusta ei löydy tai se on poistettu"
 if item["user_id"] == session["user_id"]:
  return "VIRHE: et voi lähettää viestiä omaan ilmoitukseesi"
 return render_template("new_message.html", item=item)

@app.route("/send_message/<int:item_id>", methods=["POST"])
def send_message(item_id):
 if not require_login():
  return redirect("/login")
 check_csrf()
 item = items.get_item(item_id)
 if not item:
  return "VIRHE: ilmoitusta ei löydy tai se on poistettu"
 if item["user_id"] == session["user_id"]:
  return "VIRHE: et voi lähettää viestiä omaan ilmoitukseesi"
 content = request.form["content"].strip()
 if not content:
  return render_template(
   "new_message.html",
   item=item,
   error="Viesti puuttuu"
  )
 
 if len(content) > MAX_MESSAGE_LENGTH:
  return render_template(
   "new_message.html",
   item=item,
   error="Viesti on liian pitkä"
  )
 
 message_queries.add_message(
  session["user_id"],
  item["user_id"],
  item_id,
  content
 )
 return redirect("/messages")

@app.route("/user/<int:user_id>")
def show_user(user_id):
 user = users.get_user(user_id)
 if not user:
  return "VIRHE: käyttäjää ei löytynyt"
 user_items = users.get_items(user_id)
 return render_template("user.html", user=user, items=user_items)

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
  return render_template(
   "new_item.html",
   categories=categories,
   error="Otsikko puuttuu",
   form=form
  )
 
 if len(title) > MAX_TITLE_LENGTH:
  return render_template(
   "new_item.html",
   categories=categories,
   error="Otsikko on liian pitkä",
   form=form
  )
 
 if not description:
  return render_template(
   "new_item.html",
   categories=categories,
   error="Kuvaus puuttuu",
   form=form
  )
 
 if len(description) > MAX_DESCRIPTION_LENGTH:
  return render_template(
   "new_item.html",
   categories=categories,
   error="Kuvaus on liian pitkä",
   form=form
  )
 
 if len(location) > MAX_LOCATION_LENGTH:
  return render_template(
   "new_item.html",
   categories=categories,
   error="Sijainti on liian pitkä",
   form=form
  )
 
 if not reward:
  return render_template(
   "new_item.html",
   categories=categories,
   error="Palkkio puuttuu",
   form=form
  )
 
 if category not in categories:
  return render_template(
   "new_item.html",
   categories=categories,
   error="Virheellinen luokitus",
   form=form
  )
 
 try:
  reward_value = int(reward)
 except ValueError:
  return render_template(
   "new_item.html",
   categories=categories,
   error="Palkkion pitää olla kokonaisluku",
   form=form
  )
 
 if reward_value < 0:
  return render_template(
   "new_item.html",
   categories=categories,
   error="Palkkio ei voi olla negatiivinen",
   form=form
  )
 
 items.add_item(
  title,
  description,
  reward_value,
  location,
  category,
  session["user_id"]
 )
 return redirect("/")

@app.route("/item/<int:item_id>")
def show_item(item_id):
 item = items.get_item(item_id)
 if not item:
  return "VIRHE: ilmoitusta ei löydy tai se on poistettu"
 return render_template("show_item.html", item=item)

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
 if not require_login():
  return redirect("/login")
 item = items.get_item(item_id)
 if not item:
  return "VIRHE: ilmoitusta ei löydy tai se on poistettu"
 if item["user_id"] != session["user_id"]:
  return "VIRHE: ei oikeutta muokata tätä ilmoitusta"
 return render_template("edit_item.html", item=item, categories=categories)

@app.route("/update_item/<int:item_id>", methods=["POST"])
def update_item(item_id):
 if not require_login():
  return redirect("/login")
 check_csrf()
 item = items.get_item(item_id)
 if not item:
  return "VIRHE: ilmoitusta ei löydy tai se on poistettu"
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
  return render_template(
   "edit_item.html",
   item=form,
   categories=categories,
   error="Otsikko puuttuu"
  )
 if len(title) > MAX_TITLE_LENGTH:
  return render_template(
   "edit_item.html",
   item=form,
   categories=categories,
   error="Otsikko on liian pitkä"
  )
 
 if not description:
  return render_template(
   "edit_item.html",
   item=form,
   categories=categories,
   error="Kuvaus puuttuu"
  )
 
 if len(description) > MAX_DESCRIPTION_LENGTH:
  return render_template(
   "edit_item.html",
   item=form,
   categories=categories,
   error="Kuvaus on liian pitkä"
  )
 
 if len(location) > MAX_LOCATION_LENGTH:
  return render_template(
   "edit_item.html",
   item=form,
   categories=categories,
   error="Sijainti on liian pitkä"
  )
 
 if not reward:
  return render_template(
   "edit_item.html",
   item=form,
   categories=categories,
   error="Palkkio puuttuu"
  )
 
 if category not in categories:
  return render_template(
   "edit_item.html",
   item=form,
   categories=categories,
   error="Virheellinen luokitus"
  )
 
 try:
  reward_value = int(reward)
 except ValueError:
  return render_template(
   "edit_item.html",
   item=form,
   categories=categories,
   error="Palkkion pitää olla kokonaisluku"
  )
 
 if reward_value < 0:
  return render_template(
   "edit_item.html",
   item=form,
   categories=categories,
   error="Palkkio ei voi olla negatiivinen"
  )
 
 items.update_item(
  item_id,
  title,
  description,
  reward_value,
  location,
  category
 )

 return redirect("/item/" + str(item_id))

@app.route("/delete_item/<int:item_id>", methods=["POST"])
def delete_item(item_id):
 if not require_login():
  return redirect("/login")
 check_csrf()
 item = items.get_item(item_id)
 if not item:
  return "VIRHE: ilmoitusta ei löydy tai se on poistettu"
 if item["user_id"] != session["user_id"]:
  return "VIRHE: ei oikeutta poistaa tätä ilmoitusta"
 items.delete_item(item_id)
 return redirect("/")