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
    response_mime_type="application/json",
    response_schema=gemini_recipe_schema,
    temperature=0.4,
)


def generate_recipe_from_ai(query: str) -> dict:
    """Searches the context in the database and generates a recipe."""
    try:
        embed_response = client.models.embed_content(
            model=EMBEDDING_MODEL, contents=query
        )
        query_vector = embed_response.embeddings[0].values  # type: ignore

        results = knowledge_collection.query(
            query_embeddings=[query_vector],  # type: ignore
            n_results=2,
        )

        retrieved_context = ""
        if results["documents"] and results["documents"][0]:
            retrieved_context = "\n\n".join(results["documents"][0])

        rag_prompt = f"""
        You are a professional culinary assistant. Your goal is to provide high-quality recipes based on the provided Knowledge Base context.
        
        Knowledge Base:
        {retrieved_context}
        
        User Query: {query}
        
        ABSOLUTE RULES:
        1. PRIORITIZE KNOWLEDGE BASE: Always use the data from the Knowledge Base as your primary source.
        2. FALLBACK TO INTERNAL KNOWLEDGE: If the Knowledge Base contains no information relevant to the user's query, use your own internal training data to provide a high-quality, relevant recipe.
        3. SUPPLEMENT MISSING DETAILS: If a recipe is found in the Knowledge Base but is missing required details (such as macronutrients, prep time, or specific steps) needed to complete the JSON schema, supplement the missing information using your internal knowledge.
        4. LANGUAGE: Always respond in user query language.
        """

        response = client.models.generate_content(
            model=LLM_MODEL,
            contents=rag_prompt,
            config=generation_config,
        )

        return json.loads(response.text)  # type: ignore
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update error: {str(e)}")


def refine_recipe_with_ai(current_recipe: dict, refinement: str) -> dict:
    """Makes changes to an existing recipe."""
    try:
        refine_prompt = f"""
        Current Recipe (JSON format):
        {json.dumps(current_recipe, ensure_ascii=False)}

        User's requested modification: "{refinement}"

        Instructions:
        1. Update the recipe according to the user's request while maintaining the original JSON structure.
        2. If ingredients are added, removed, or their amounts are changed, you MUST recalculate the macronutrients (calories, protein, fats, and carbohydrates) to ensure accuracy.
        3. Ensure that all text content (title, description, steps, etc.) remains in user query language.
        4. Return the result strictly as a valid JSON object. Do not include any conversational text or markdown formatting.
        """

        response = client.models.generate_content(
            model=LLM_MODEL, contents=refine_prompt, config=generation_config
        )
        return json.loads(response.text)  # type: ignore
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update error: {str(e)}")
