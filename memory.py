
import sqlite3

# ---------- DATABASE CONNECTION ----------

conn = sqlite3.connect("memory.db", check_same_thread=False)
cursor = conn.cursor()


# ---------- TABLES ----------

cursor.execute("""
CREATE TABLE IF NOT EXISTS conversation_memory (
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


# ---------- CONVERSATION MEMORY ----------

def remember(role, content):

    cursor.execute(
        "INSERT INTO conversation_memory (role, content) VALUES (?, ?)",
        (role, content)
    )

    conn.commit()


def recall(limit=10):

    cursor.execute(
        "SELECT role, content FROM conversation_memory ORDER BY rowid DESC LIMIT ?",
        (limit,)
    )

    rows = cursor.fetchall()

    conversation = ""

    for role, content in reversed(rows):
        conversation += f"{role}: {content}\n"

    return conversation


def clear_chat_memory():

    cursor.execute("DELETE FROM conversation_memory")

    conn.commit()


# ---------- PERSONAL MEMORY ----------

def save_personal(key, value):

    cursor.execute(
        "INSERT OR REPLACE INTO personal_memory (key, value) VALUES (?, ?)",
        (key, value)
    )

    conn.commit()


def get_personal():

    cursor.execute("SELECT key, value FROM personal_memory")

    rows = cursor.fetchall()

    data = {}

    for key, value in rows:
        data[key] = value

    return data
