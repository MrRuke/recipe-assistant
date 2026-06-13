from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import recipes, settings

app = FastAPI(title="PP Recipes AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recipes.router)
app.include_router(settings.router)


@app.get("/")
async def root():
    return {"message": "API works"}
