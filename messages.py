import db

def add_message(sender_id, receiver_id, item_id, content):
    sql = """
        INSERT INTO messages (sender_id, receiver_id, item_id, content)
        VALUES (?, ?, ?, ?)
    """
    db.execute(sql, [sender_id, receiver_id, item_id, content])

def get_messages(user_id):
    sql = """
        SELECT messages.id,
               messages.content,
               messages.created_at,
               messages.sender_id,
               messages.receiver_id,
               messages.item_id,
               sender.username sender_username,
               receiver.username receiver_username,
               items.title item_title
        FROM messages, users sender, users receiver, items
        WHERE messages.sender_id = sender.id
          AND messages.receiver_id = receiver.id
          AND messages.item_id = items.id
          AND (messages.sender_id = ? OR messages.receiver_id = ?)
        ORDER BY messages.id DESC
    """
    return db.query(sql, [user_id, user_id])