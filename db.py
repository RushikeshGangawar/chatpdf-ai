import sqlite3

def init_db():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT
        )
    ''')

    conn.commit()
    conn.close()


def save_chat(q, a):
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO chat (question, answer) VALUES (?, ?)",
        (q, a)
    )

    conn.commit()
    conn.close()
