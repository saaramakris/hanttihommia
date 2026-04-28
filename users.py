from werkzeug.security import check_password_hash, generate_password_hash

import db

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

def get_items(user_id):
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
    return db.query(sql, [user_id])

def create_user(username, password):
    password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, username, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if len(result) == 0:
        return None

    user = result[0]

    if check_password_hash(user["password_hash"], password):
        return user

    return None