from typing import List, Optional

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


class UserSettingsSchema(BaseModel):
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    goal: str = "maintain"
