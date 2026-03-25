import json
import os

from dotenv import load_dotenv
from google.genai import Client, types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = Client(api_key=api_key)

recipe_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "Название блюда"},
        "description": {"type": "string", "description": "Краткое описание"},
        "macros": {
            "type": "object",
            "properties": {
                "calories": {"type": "integer"},
                "protein_g": {"type": "integer"},
                "fat_g": {"type": "integer"},
                "carbs_g": {"type": "integer"},
            },
            "required": ["calories", "protein_g", "fat_g", "carbs_g"],
        },
        "prep_time_minutes": {
            "type": "integer",
            "description": "Время приготовления в минутах",
        },
        "ingredients": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "amount": {
                        "type": "string",
                        "description": "Граммовка (например: 150г, 2 ст.л.)",
                    },
                },
                "required": ["name", "amount"],
            },
        },
        "steps": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Пошаговая инструкция",
        },
        "substitutions": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Возможные замены ингредиентов (например: Курицу можно заменить на индейку)",
        },
    },
    "required": [
        "title",
        "description",
        "macros",
        "prep_time_minutes",
        "ingredients",
        "steps",
        "substitutions",
    ],
}

generation_config = types.GenerateContentConfig(
    # system_instruction=system_instruction,
    response_mime_type="application/json",
    response_schema=recipe_schema,
    temperature=0.4,
)


def start_recipe_creation():
    chat = client.chats.create(model="gemini-2.5-flash", config=generation_config)

    system_instruction = "Ты профессиональный диетолог. Составляй и корректируй ПП-рецепты по запросу пользователя. Обязательно возвращай ответ строго в требуемом JSON формате."

    query = input(
        "Какой ПП-рецепт тебе нужен? (например: ужин с говядиной до 400 ккал):\n> "
    )
    print("\nГенерирую первый вариант рецепта...")
    response = chat.send_message(
        message=f"{system_instruction}\nЗапрос: {query}", config=generation_config
    )
    recipe_data = json.loads(response.text)

    MAX_REVISIONS = 2

    print("\n=== ОБНОВЛЕННЫЙ РЕЦЕПТ ===")
    print(json.dumps(recipe_data, indent=4, ensure_ascii=False))
    print("===================\n")

    for i in range(MAX_REVISIONS):
        refinement = input(
            f"Есть ли пожелания по изменению? (Осталось правок: {MAX_REVISIONS - i}).\nНапиши, что изменить, или нажми Enter, чтобы продолжить без изменений:\n> "
        )

        if not refinement.strip():
            print("Оставляем текущий вариант.")
            break

        print(f"\nОбновляю рецепт с учетом: '{refinement}'...")

        response = chat.send_message(
            f"Измени предыдущий рецепт с учетом этого пожелания: {refinement}. Пересчитай КБЖУ и время, если требуется. Верни полностью обновленный рецепт в формате JSON."
        )
        recipe_data = json.loads(response.text)

        print("\n=== ОБНОВЛЕННЫЙ РЕЦЕПТ ===")
        print(json.dumps(recipe_data, indent=4, ensure_ascii=False))
        print("===================\n")

    save_choice = input("Сохранить итоговый вариант в избранное? (y/n): ")
    if save_choice.lower() == "y":
        print("\n[Симуляция] Рецепт успешно сохранен в базу данных!")


if __name__ == "__main__":
    try:
        start_recipe_creation()

    except Exception as e:
        print(f"Произошла ошибка: {e}")
