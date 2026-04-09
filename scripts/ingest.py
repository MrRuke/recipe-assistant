import os

import chromadb
from dotenv import load_dotenv
from google.genai import Client
from pypdf import PdfReader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CHROMA_DB_PATH = os.path.join(DATA_DIR, "chroma_db")
EMBEDDING_MODEL = "gemini-embedding-001"

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = Client(api_key=api_key)
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)


try:
    # chroma_client.delete_collection("pp_recipes_knowledge")
    print("The old base has been cleared..")
except ValueError:
    pass

collection = chroma_client.get_or_create_collection(name="pp_recipes_knowledge")


def embed_and_store(file_path):
    print(f"Reading file {file_path}...")

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = text.split("\n\n")
    chunks = [c.strip() for c in chunks if len(c.strip()) > 50]

    print(f"{len(chunks)} fragments found. Starting vectorization...")

    for i, chunk in enumerate(chunks):
        response = client.models.embed_content(
            model="gemini-embedding-001", contents=chunk
        )
        vector = response.embeddings[0].values  # type: ignore

        collection.add(
            embeddings=[vector],  # type: ignore
            documents=[chunk],
            ids=[f"recipe_chunk_{i}"],
        )
        print(f"Fragment saved {i + 1}/{len(chunks)}")

    print("✅ Knowledge base successfully created!")


def extract_text_from_pdf(pdf_path):
    """Reads PDF and merges text from all pages."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text


def embed_and_store_pdf(filename):
    file_path = os.path.join(DATA_DIR, filename)
    print(f"\nI'm starting to process the book: {file_path}")

    if not os.path.exists(file_path):
        print(f"❌ ERROR: File {filename} not found in data/!")
        return

    full_text = extract_text_from_pdf(file_path)
    raw_paragraphs = full_text.split("\n\n")
    chunks = []
    current_chunk = ""

    for para in raw_paragraphs:
        if len(current_chunk) > 800:
            chunks.append(current_chunk.strip())
            current_chunk = para
        else:
            current_chunk += "\n\n" + para

    if current_chunk:
        chunks.append(current_chunk.strip())

    chunks = [c for c in chunks if len(c) > 50]
    print(f"Split into {len(chunks)} fragments. Vectorizing...")

    for i, chunk in enumerate(chunks):
        try:
            response = client.models.embed_content(
                model=EMBEDDING_MODEL, contents=chunk
            )
            vector = response.embeddings[0].values  # type: ignore

            safe_filename = filename.replace(".pdf", "").replace(" ", "_")
            unique_id = f"{safe_filename}_chunk_{i}"

            collection.add(
                embeddings=[vector],  # type: ignore
                documents=[chunk],
                metadatas=[{"source": filename}],
                ids=[unique_id],
            )
        except Exception as e:
            print(f"Error on fragment {i + 1}: {e}")

    print(f"✅ Book '{filename}' successfully uploaded to the database!")


if __name__ == "__main__":
    BOOKS = ["book1.pdf"]

    for book in BOOKS:
        embed_and_store_pdf(book)
