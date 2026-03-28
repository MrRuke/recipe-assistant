import os

import chromadb
from dotenv import load_dotenv
from google.genai import Client
from pypdf import PdfReader

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = Client(api_key=api_key)

chroma_client = chromadb.PersistentClient(path="./chroma_db")


try:
    chroma_client.delete_collection("pp_recipes_knowledge")
    print("Старая база данных очищена.")
except ValueError:
    pass

collection = chroma_client.get_or_create_collection(name="pp_recipes_knowledge")


def embed_and_store(file_path):
    print(f"Читаю файл {file_path}...")

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = text.split("\n\n")
    chunks = [c.strip() for c in chunks if len(c.strip()) > 50]

    print(f"Найдено {len(chunks)} фрагментов. Начинаю векторизацию...")

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
        print(f"Сохранен фрагмент {i + 1}/{len(chunks)}")

    print("✅ База знаний успешно создана!")


def extract_text_from_pdf(pdf_path):
    """Читает PDF и склеивает текст со всех страниц."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text


def embed_and_store_pdf(file_path):
    print(f"Читаю PDF файл: {file_path}...")
    full_text = extract_text_from_pdf(file_path)

    # 3. Умная нарезка (Chunking)
    # Разбиваем текст по абзацам и склеиваем в блоки примерно по 800 символов
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

    # Убираем слишком короткие куски (мусор вроде номеров страниц)
    chunks = [c for c in chunks if len(c) > 50]

    print(
        f"Текст извлечен и разбит на {len(chunks)} фрагментов. Начинаю векторизацию..."
    )

    # 4. Векторизация и сохранение
    for i, chunk in enumerate(chunks):
        try:
            response = client.models.embed_content(
                model="gemini-embedding-001", contents=chunk
            )
            vector = response.embeddings[0].values  # type: ignore

            collection.add(
                embeddings=[vector],  # type: ignore
                documents=[chunk],
                ids=[f"pdf_chunk_{i}"],
            )
            print(f"Сохранен фрагмент {i + 1}/{len(chunks)}")
        except Exception as e:
            print(f"Ошибка на фрагменте {i + 1}: {e}")

    print("\n✅ База знаний из PDF успешно создана и готова к работе!")


if __name__ == "__main__":
    # embed_and_store("recipe_book.txt")
    embed_and_store_pdf("book1.pdf")
