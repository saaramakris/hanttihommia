import db


def add_message(sender_id, receiver_id, item_id, content):
    sql = """
        INSERT INTO messages (sender_id, receiver_id, item_id, content)
        VALUES (?, ?, ?, ?)
    """
    db.execute(sql, [sender_id, receiver_id, item_id, content])

    message_id = db.last_insert_id()

    sql = """
        UPDATE messages
        SET thread_id = ?
        WHERE id = ?
    """
    db.execute(sql, [message_id, message_id])


def add_reply(thread_id, sender_id, receiver_id, item_id, content):
    sql = """
        INSERT INTO messages (sender_id, receiver_id, item_id, content, thread_id)
        VALUES (?, ?, ?, ?, ?)
    """
    db.execute(sql, [sender_id, receiver_id, item_id, content, thread_id])


def get_messages(user_id):
    sql = """
        SELECT latest_message.id,
               latest_message.content,
               latest_message.created_at,
               latest_message.sender_id,
               latest_message.receiver_id,
               latest_message.item_id,
               latest_message.thread_id,
               sender.username sender_username,
               receiver.username receiver_username,
               items.title item_title
        FROM messages latest_message, users sender, users receiver, items
        WHERE latest_message.sender_id = sender.id
          AND latest_message.receiver_id = receiver.id
          AND latest_message.item_id = items.id
          AND latest_message.id IN (
              SELECT MAX(id)
              FROM messages
              WHERE sender_id = ? OR receiver_id = ?
              GROUP BY thread_id
          )
        ORDER BY latest_message.id DESC
    """
    return db.query(sql, [user_id, user_id])


def get_thread(thread_id, user_id):
    sql = """
        SELECT messages.id,
               messages.content,
               messages.created_at,
               messages.sender_id,
               messages.receiver_id,
               messages.item_id,
               messages.thread_id,
               sender.username sender_username,
               receiver.username receiver_username,
               items.title item_title
        FROM messages, users sender, users receiver, items
        WHERE messages.sender_id = sender.id
          AND messages.receiver_id = receiver.id
          AND messages.item_id = items.id
          AND messages.thread_id = ?
          AND (messages.sender_id = ? OR messages.receiver_id = ?)
        ORDER BY messages.id
    """
    return db.query(sql, [thread_id, user_id, user_id])