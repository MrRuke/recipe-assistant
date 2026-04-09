# AI Recipe Assistant (RAG-based)

An intelligent culinary assistant that learns from your personal PDF cookbooks using Retrieval-Augmented Generation (RAG). Instead of relying on generic AI knowledge, this system provides accurate recipes directly from your own sources.

## 🚀 Key Features
- **RAG Engine:** Automatically retrieves relevant context from PDF books using vector similarity search.
- **Smart Parsing:** Processes complex PDF layouts and splits them into meaningful segments for the AI.
- **Strict JSON Output:** Leverages Gemini's structured output to ensure recipe data (ingredients, steps, macros) is always valid and consistent.
- **Interactive UI:** Allows users to ask for modifications (e.g., "make it vegan" or "double the protein") while keeping the original context.
- **Digital Cookbook Catalog:** Automatically extracts a clickable catalog of recipes from the books' tables of contents.
- **Favorites System**: Save your favorite generated recipes to a local SQLite database.

## 🛠 Tech Stack
- **Frontend:** Angular 17+, TypeScript, CSS3
- **Backend:** Python 3.10+, FastAPI, Uvicorn
- **AI/LLM:** Google Gemini 2.5 Flash API
- **Vector Database:** ChromaDB
- **Database:** SQLite (for persistent storage of saved recipes)
- **PDF Processing**: PyPDF.

## 📋 System Architecture
1. **Ingestion Layer:** PDF documents are parsed, converted into embeddings using text-embedding-004, and stored in a ChromaDB vector store.
2. **Retrieval Layer:** When a user queries a recipe, the system calculates the semantic vector of the query and finds the top-K relevant passages in the vector store.
3. **Augmentation Layer:** The retrieved text is injected into a specialized English system prompt.
4. **Generation Layer:** Gemini processes the prompt and returns a structured JSON object representing the recipe.

## ⚙️ Setup & Installation

### 1. Clone the Repository
```
git clone https://github.com/MrRuke/ai-recepie
cd ai-recepie
```
### 2. Backend Setup (Python)
It is recommended to use a virtual environment:
```python
python -m venv .venv
# Activate on Windows:
.venv\Scripts\activate
# Activate on Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```
### 3. Frontend Setup (Angular)
```
cd frontend
npm install
cd ..
```
### 4. Configuration
Create a file at `.env` with your credentials:
```
GEMINI_API_KEY = "your_google_gemini_api_key"
```
### 5. Ingest Your Knowledge Base
Place your PDF cookbooks into the `data/` folder, then run:
```python
# Indexes the content into the vector database
python scripts/ingest.py

# Generates the clickable catalog for the UI
python scripts/extract_catalog.py
```
### 6. Run the Application
Use the unified launcher to start both the backend and frontend simultaneously:
```python
python start_all.py
```

## 🧠 Lessons Learned
- Implementing RAG (Retrieval-Augmented Generation) to reduce AI hallucinations.
- Managing vector embeddings and semantic search workflows.
- Designing a modular clean architecture in FastAPI (Routers, Services, Schemas).
- Handling asynchronous API calls and state management in Angular.
- Fine-tuning LLM prompts to output strictly formatted JSON data.