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
    print("Reading...")
    reader = PdfReader(pdf_path)
    text = ""
    for page_num in pages_to_read:
        if page_num < len(reader.pages):
            text += reader.pages[page_num].extract_text() + "\n"
    return text


def generate_catalog_json(text):
    print("Generating...")

    prompt = f"""
    Below is the Table of Contents text from a cookbook:
    {text}
    
    Task:
    Extract ONLY the recipe titles and their corresponding category headings (group names). 
    Strictly ignore page numbers, introductions, chapter numbers, author's notes, and any other metadata.
    
    Format:
    Return the result strictly as a valid JSON array of objects. Each object should represent a category.
    Example format:
    [
      {{
        "groupName": "Breakfast",
        "values": ["Syriki (Cheese Pancakes)", "Vegetable Omelet"]
      }},
      {{
        "groupName": "Main Dishes",
        "values": ["Baked Salmon", "Chicken Stir-fry"]
      }}
    ]
    
    Constraint:
    Do not include any conversational text, explanations, or markdown formatting blocks. Return only the raw JSON.
    """

    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

    clean_text = response.text.replace("```json", "").replace("```", "").strip()  # type: ignore
    return json.loads(clean_text)


if __name__ == "__main__":
    master_catalog = []
    for pdf_file, toc_pages in BOOKS_TOC.items():
        print(f"\n🔍 Extracting recipes from the table of contents: {pdf_file}")
        try:
            toc_text = extract_toc_text(pdf_file, toc_pages)
            catalog_list = generate_catalog_json(toc_text)
            master_catalog.extend(catalog_list)
            print(f"Added {len(catalog_list)} recipes from this book.")
        except Exception as e:
            print(f"❌ Error while processing {pdf_file}: {e}")

    master_catalog = list(set(master_catalog))
    master_catalog.sort()

    with open("catalog.json", "w", encoding="utf-8") as f:
        json.dump(master_catalog, f, ensure_ascii=False, indent=4)

    print(
        f"\n✅ Done! A total of {len(master_catalog)} unique recipes have been collected from all books. Saved in catalog.json"
    )
