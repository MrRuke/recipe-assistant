import sqlite3

import chromadb

from .config import CHROMA_DB_PATH, SQLITE_DB_PATH


def init_sqlite():
    conn = sqlite3.connect(SQLITE_DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_query TEXT,
            recipe_json TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            height_cm REAL,
            weight_kg REAL,
            goal TEXT DEFAULT 'maintain',
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        INSERT OR IGNORE INTO user_settings (id, height_cm, weight_kg, goal)
        VALUES (1, NULL, NULL, 'maintain')
    """)
    conn.commit()
    return conn


sqlite_conn = init_sqlite()

chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
knowledge_collection = chroma_client.get_or_create_collection(
    name="pp_recipes_knowledge"
)
