import sqlite3

DB_PATH = "marketing.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            audience TEXT,
            content TEXT,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_campaign(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT INTO campaigns (product, audience, content, image_path)
        VALUES (?, ?, ?, ?)
    """, (
        data["product"],
        data["audience"],
        data["content"],
        data.get("image_path")
    ))

    conn.commit()
    conn.close()


def get_campaigns():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM campaigns ORDER BY created_at DESC")
    rows = c.fetchall()

    conn.close()
    return rows