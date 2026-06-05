import json
import os

from fastapi import APIRouter, HTTPException

from ..ai_service import generate_recipe_from_ai, refine_recipe_with_ai
from ..config import CATALOG_PATH
from ..database import sqlite_conn
from ..schemas import GenerateRequest, RefineRequest, SaveRequest

router = APIRouter(prefix="/api/recipes", tags=["Recipes"])


@router.post("/generate")
async def generate_recipe(req: GenerateRequest):
    return generate_recipe_from_ai(req.query)


@router.post("/refine")
async def refine_recipe(req: RefineRequest):
    return refine_recipe_with_ai(req.current_recipe, req.refinement)


@router.post("/save")
async def save_recipe(req: SaveRequest):
    try:
        cursor = sqlite_conn.cursor()
        cursor.execute(
            "INSERT INTO saved_recipes (original_query, recipe_json) VALUES (?, ?)",
            (req.original_query, json.dumps(req.recipe_data, ensure_ascii=False)),
        )
        sqlite_conn.commit()
        return {"status": "success", "message": "Рецепт сохранен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка БД: {str(e)}")


@router.get("/favorites")
async def get_favorites():
    try:
        cursor = sqlite_conn.cursor()
        cursor.execute(
            "SELECT id, original_query, recipe_json, created_at FROM saved_recipes ORDER BY id DESC"
        )
        rows = cursor.fetchall()

        favorites = []
        for row in rows:
            favorites.append(
                {
                    "id": row[0],
                    "original_query": row[1],
                    "recipe_data": json.loads(row[2]),
                    "created_at": row[3],
                }
            )
        return {"favorites": favorites}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка чтения БД: {str(e)}")


@router.delete("/favorites/{recipe_id}")
async def delete_favorite(recipe_id: int):
    try:
        cursor = sqlite_conn.cursor()
        cursor.execute("DELETE FROM saved_recipes WHERE id = ?", (recipe_id,))
        sqlite_conn.commit()
        return {"status": "success", "message": "Рецепт удален из избранного"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка БД: {str(e)}")


@router.get("/catalog")
async def get_catalog():
    if not os.path.exists(CATALOG_PATH):
        return {"catalog": []}
    try:
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        return {"catalog": catalog}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка каталога: {str(e)}")
