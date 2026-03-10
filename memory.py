import sqlite3

DB_FILE = "memory.db"


# ---------- DATABASE CONNECTION ----------
def get_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)


# ---------- INITIALIZE DATABASE ----------
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversation_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        content TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS personal_memory (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    conn.commit()
    conn.close()


# ---------- CONVERSATION MEMORY ----------

def remember(role, content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO conversation_memory (role, content) VALUES (?, ?)",
        (role, content)
    )

    conn.commit()
    conn.close()


def recall(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role, content FROM conversation_memory ORDER BY rowid DESC LIMIT ?",
        (limit,)
    )

    rows = cursor.fetchall()
    conn.close()

    conversation = ""

    for role, content in reversed(rows):
        conversation += f"{role}: {content}\n"

    return conversation


def clear_chat_memory():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM conversation_memory")

    conn.commit()
    conn.close()


# ---------- PERSONAL MEMORY ----------

def save_personal(key, value):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR REPLACE INTO personal_memory (key, value) VALUES (?, ?)",
        (key, value)
    )

    conn.commit()
    conn.close()


def get_personal():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT key, value FROM personal_memory")

    rows = cursor.fetchall()
    conn.close()

    data = {}

    for key, value in rows:
        data[key] = value

    return data