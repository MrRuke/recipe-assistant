import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

CHROMA_DB_PATH = os.path.join(DATA_DIR, "chroma_db")
SQLITE_DB_PATH = os.path.join(DATA_DIR, "pp_recipes.db")
CATALOG_PATH = os.path.join(DATA_DIR, "catalog.json")

LLM_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "gemini-embedding-001"
