import json
import os
import sqlite3
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

import chromadb
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.genai import Client, types
from pydantic import BaseModel

load_dotenv()

DB_NAME = "pp_recipes.db"

api_key = os.getenv("GEMINI_API_KEY")
client = Client(api_key=api_key)

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="pp_recipes_knowledge")

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


system_instruction = "Ты профессиональный диетолог. Составляй и корректируй ПП-рецепты по запросу пользователя. Обязательно возвращай ответ строго в требуемом JSON формате."

generation_config = types.GenerateContentConfig(
    system_instruction=system_instruction,
    response_mime_type="application/json",
    response_schema=recipe_schema,
    temperature=0.4,
)


class GenerateRequest(BaseModel):
    query: str


class RefineRequest(BaseModel):
    current_recipe: Dict[str, Any]
    refinement: str


class SaveRequest(BaseModel):
    original_query: str
    recipe_data: Dict[str, Any]


for model in client.models.list():
    # Ищем модели, которые поддерживают метод embedContent
    if model.supported_actions and "embedContent" in model.supported_actions:
        print(model.name)
    # print(model.name)
    # print(model.supported_actions)


@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorite_recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_query TEXT NOT NULL,
            recipe_title TEXT NOT NULL,
            recipe_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

    yield


app = FastAPI(title="PP Recipes API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/recipes/generate")
async def generate_recipe(req: GenerateRequest):
    try:
        embed_response = client.models.embed_content(
            model="gemini-embedding-001", contents=req.query
        )
        query_vector = embed_response.embeddings[0].values  # type: ignore

        results = collection.query(
            query_embeddings=[query_vector],  # type: ignore
            n_results=2,
        )

        retrieved_context = "\n\n".join(results["documents"][0])  # type: ignore

        print("\n=== ЧТО ДОСТАЛИ ИЗ БАЗЫ (RAG КОНТЕКСТ) ===")
        print(retrieved_context)
        print("==========================================\n")

        rag_prompt = f"""
        Запрос пользователя: {req.query}
        
        Вот рецепты из нашей базы знаний:
        {retrieved_context}
        
        Твоя задача:
        1. Выбери наиболее подходящий рецепт из предоставленной базы знаний.
        2. Сформируй ответ строго на основе этого рецепта в нужном JSON формате.
        3. Если в базе знаний нет подходящего ответа, адаптируй ближайший рецепт из базы, но не выдумывай совершенно новые блюда.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=rag_prompt, config=generation_config
        )
        if not response.text:
            raise HTTPException(status_code=500, detail="Модель вернула пустой ответ.")

        return json.loads(response.text)
        #
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Запрос: {req.query}",
            config=generation_config,
        )
        if not response.text:
            raise HTTPException(
                status_code=500,
                detail="Модель вернула пустой ответ (возможно, сработал фильтр безопасности).",
            )
        return json.loads(response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/recipes/catalog")
async def get_catalog():
    """Отдает список всех рецептов из оглавления."""
    catalog_path = "catalog.json"
    if not os.path.exists(catalog_path):
        return {"catalog": []}

    try:
        with open(catalog_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        return {"catalog": catalog}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка чтения каталога: {e}")


@app.post("/api/recipes/refine")
async def refine_recipe(req: RefineRequest):
    try:
        prompt = f"Вот текущий рецепт:\n{json.dumps(req.current_recipe, ensure_ascii=False)}\n\nПожелание по изменению: {req.refinement}\n\nВерни полностью обновленный рецепт, пересчитав КБЖУ и шаги, если это необходимо."

        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt, config=generation_config
        )
        if not response.text:
            raise HTTPException(
                status_code=500,
                detail="Модель вернула пустой ответ (возможно, сработал фильтр безопасности).",
            )
        return json.loads(response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/recipes/save")
async def save_recipe(req: SaveRequest):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        title = req.recipe_data.get("title", "Без названия")
        json_string = json.dumps(req.recipe_data, ensure_ascii=False)

        cursor.execute(
            """
            INSERT INTO favorite_recipes (original_query, recipe_title, recipe_json)
            VALUES (?, ?, ?)
        """,
            (req.original_query, title, json_string),
        )
        conn.commit()
        conn.close()
        return {"status": "success", "message": f"Рецепт '{title}' сохранен."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/recipes/favorites")
async def get_favorites():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, recipe_title, recipe_json, created_at FROM favorite_recipes ORDER BY id DESC"
        )
        rows = cursor.fetchall()
        conn.close()

        favorites = [
            {
                "id": r[0],
                "title": r[1],
                "recipe_data": json.loads(r[2]),
                "created_at": r[3],
            }
            for r in rows
        ]
        return {"favorites": favorites}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
