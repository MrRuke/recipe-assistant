from typing import List

from pydantic import BaseModel


class GenerateRequest(BaseModel):
    query: str


class RefineRequest(BaseModel):
    current_recipe: dict
    refinement: str


class SaveRequest(BaseModel):
    original_query: str
    recipe_data: dict


class RecipeSchema(BaseModel):
    title: str
    description: str
    macros: dict
    prep_time_minutes: int
    ingredients: List[dict]
    steps: List[str]
    substitutions: List[str]
