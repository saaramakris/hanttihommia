DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    reward INTEGER NOT NULL,
    location TEXT,
    category TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL REFERENCES users,
    deleted INTEGER DEFAULT 0
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    sender_id INTEGER NOT NULL REFERENCES users,
    receiver_id INTEGER NOT NULL REFERENCES users,
    item_id INTEGER NOT NULL REFERENCES items,
    thread_id INTEGER REFERENCES messages
);