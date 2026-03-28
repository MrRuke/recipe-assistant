import json
import os

from dotenv import load_dotenv
from google.genai import Client
from pypdf import PdfReader

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = Client(api_key=api_key)

BOOKS_TOC = {
    "book1.pdf": [4, 5, 6],
}


def extract_toc_text(pdf_path, pages_to_read):
    print("Читаю страницы оглавления...")
    reader = PdfReader(pdf_path)
    text = ""
    for page_num in pages_to_read:
        if page_num < len(reader.pages):
            text += reader.pages[page_num].extract_text() + "\n"
    return text


def generate_catalog_json(text):
    print("Прошу ИИ составить чистый список рецептов...")
    prompt = f"""
    Вот текст оглавления из кулинарной книги:
    {text}
    
    Твоя задача: вытащи из этого текста ТОЛЬКО названия рецептов и название группы.
    Игнорируй номера страниц, введения, главы, слова автора и прочий мусор.
    Верни результат строго в формате валидного JSON-массива строк. сгруппированных по группам 
    Пример: ["groupName:" Завтраки, values: ["Сырники", "Омлет с овощами"]]
    Не пиши никаких пояснений, только JSON.
    """

    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

    clean_text = response.text.replace("```json", "").replace("```", "").strip()  # type: ignore
    return json.loads(clean_text)


if __name__ == "__main__":
    master_catalog = []
    for pdf_file, toc_pages in BOOKS_TOC.items():
        print(f"\n🔍 Извлекаю рецепты из оглавления: {pdf_file}")
        try:
            toc_text = extract_toc_text(pdf_file, toc_pages)
            catalog_list = generate_catalog_json(toc_text)
            master_catalog.extend(catalog_list)
            print(f"Добавлено {len(catalog_list)} рецептов из этой книги.")
        except Exception as e:
            print(f"❌ Ошибка при обработке {pdf_file}: {e}")

    master_catalog = list(set(master_catalog))
    master_catalog.sort()

    with open("catalog.json", "w", encoding="utf-8") as f:
        json.dump(master_catalog, f, ensure_ascii=False, indent=4)

    print(
        f"\n✅ Готово! Всего собрано {len(master_catalog)} уникальных рецептов из всех книг. Сохранено в catalog.json"
    )
