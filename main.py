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


print("Доступные модели:")
for model in client.models.list():
    if "generateContent" in model.supported_actions:
        print(model.name)


def get_recipe(user_query):
    prompt = f"""
    Ты профессиональный диетолог. Составь ПП-рецепт по запросу пользователя.
    Запрос: {user_query}
    В ответе верни только сырой JSON согласно схеме.
    """

    print("Генерирую рецепт, подожди пару секунд...")
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=f"Запрос: {prompt}", config=generation_config
    )

    return json.loads(response.text)


if __name__ == "__main__":
    query = input(
        "Какой ПП-рецепт тебе нужен? (например: ужин с рыбой до 300 ккал):\n> "
    )

    try:
        recipe_data = get_recipe(query)
        print("\n=== ТВОЙ РЕЦЕПТ ===")
        print(json.dumps(recipe_data, indent=4, ensure_ascii=False))
        print("===================\n")

        save_choice = input("Сохранить в избранное? (y/n): ")
        if save_choice.lower() == "y":
            print("Здесь будет логика сохранения в SQLite!")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
