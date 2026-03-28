import json
import os

from dotenv import load_dotenv
from google.genai import Client
from pypdf import PdfReader

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = Client(api_key=api_key)

PDF_FILE = "book1.pdf"
TOC_PAGES = [4, 5, 6]


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
    try:
        toc_text = extract_toc_text(PDF_FILE, TOC_PAGES)
        catalog_list = generate_catalog_json(toc_text)

        with open("catalog.json", "w", encoding="utf-8") as f:
            json.dump(catalog_list, f, ensure_ascii=False, indent=4)

        print(
            f"✅ Готово! Найдено {len(catalog_list)} рецептов. Сохранено в catalog.json"
        )
    except Exception as e:
        print(f"❌ Ошибка: {e}")
