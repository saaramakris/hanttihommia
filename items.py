import db


def get_items():
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
          AND items.deleted = 0
        ORDER BY items.id DESC
    """
    return db.query(sql)


def search_items(query, location, category):
    like = "%" + query + "%"
    location_like = "%" + location + "%"

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
          AND items.deleted = 0
          AND (? = '' OR items.title LIKE ? OR items.description LIKE ?)
          AND (? = '' OR items.location LIKE ?)
          AND (? = '' OR items.category = ?)
        ORDER BY items.id DESC
    """
    return db.query(sql, [
        query, like, like,
        location, location_like,
        category, category
    ])


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
        WHERE items.user_id = users.id
          AND items.deleted = 0
          AND items.id = ?
    """
    result = db.query(sql, [item_id])

    if len(result) == 0:
        return None

    return result[0]


def add_item(title, description, reward, location, category, user_id):
    sql = """
        INSERT INTO items (title, description, reward, location, category, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    db.execute(sql, [title, description, reward, location, category, user_id])


def update_item(item_id, title, description, reward, location, category):
    sql = """
        UPDATE items
        SET title = ?,
            description = ?,
            reward = ?,
            location = ?,
            category = ?
        WHERE id = ?
    """
    db.execute(sql, [title, description, reward, location, category, item_id])


def delete_item(item_id):
    sql = "UPDATE items SET deleted = 1 WHERE id = ?"
    db.execute(sql, [item_id])