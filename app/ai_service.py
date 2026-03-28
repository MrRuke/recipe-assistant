import json
import os

from dotenv import load_dotenv
from fastapi import HTTPException
from google.genai import Client, types

from .config import EMBEDDING_MODEL, LLM_MODEL
from .database import knowledge_collection

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = Client(api_key=GEMINI_API_KEY)

system_instruction = "Ты профессиональный диетолог. Составляй и корректируй ПП-рецепты по запросу пользователя. Обязательно возвращай ответ строго в требуемом JSON формате."

gemini_recipe_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"},
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
        "prep_time_minutes": {"type": "integer"},
        "ingredients": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "amount": {"type": "string"},
                },
                "required": ["name", "amount"],
            },
        },
        "steps": {"type": "array", "items": {"type": "string"}},
        "substitutions": {"type": "array", "items": {"type": "string"}},
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
    system_instruction=system_instruction,
    response_mime_type="application/json",
    response_schema=gemini_recipe_schema,
    temperature=0.4,
)


def generate_recipe_from_ai(query: str) -> dict:
    """Ищет контекст в базе и генерирует рецепт."""
    try:
        embed_response = client.models.embed_content(
            model=EMBEDDING_MODEL, contents=query
        )
        query_vector = embed_response.embeddings[0].values  # type: ignore

        results = knowledge_collection.query(
            query_embeddings=[query_vector],  # type: ignore
            n_results=2,  # type: ignore
        )

        retrieved_context = ""
        if results["documents"] and results["documents"][0]:
            retrieved_context = "\n\n".join(results["documents"][0])

        print("\n=== НАЙДЕННЫЙ КОНТЕКСТ ДЛЯ ИИ ===")
        print(retrieved_context[:200] + "...\n=================================\n")

        rag_prompt = f"""
        Ты — строгий кулинарный ассистент. Твоя задача — возвращать рецепты на основе предоставленного текста (Базы знаний).
        База знаний:
        {retrieved_context}
        
        Запрос пользователя: {query}
        
        АБСОЛЮТНЫЕ ПРАВИЛА:
        1. В первую очередь используй даныне из базы знаний
        2. Если в базе знаний нет ничего релевантного запросу, то тогда дополни информацию из своей базы знани
        3. Если рецепт есть в базе знаний, но не все соответствует формату, дополни пропуски
        """

        response = client.models.generate_content(
            model=LLM_MODEL,
            contents=rag_prompt,
            config=generation_config,
        )

        return json.loads(response.text)  # type: ignore
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации: {str(e)}")


def refine_recipe_with_ai(current_recipe: dict, refinement: str) -> dict:
    """Вносит правки в существующий рецепт."""
    try:
        refine_prompt = f"""
        Вот текущий рецепт (в формате JSON):
        {json.dumps(current_recipe, ensure_ascii=False)}

        Пожелание пользователя по изменению: "{refinement}"

        Измени рецепт с учетом пожелания. Если меняются ингредиенты, пересчитай КБЖУ.
        Верни обновленный рецепт строго в JSON формате.
        """

        response = client.models.generate_content(
            model=LLM_MODEL, contents=refine_prompt, config=generation_config
        )
        return json.loads(response.text)  # type: ignore
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления: {str(e)}")
