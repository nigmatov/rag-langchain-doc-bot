from pydantic import BaseModel
import os

class Settings(BaseModel):
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    collection_name: str = os.getenv("COLLECTION", "docs")
    persist_dir: str = os.getenv("CHROMA_DIR", ".chroma")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    top_k: int = int(os.getenv("TOP_K", "4"))

settings = Settings()
