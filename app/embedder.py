from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from .settings import settings

def get_embedding_fn():
    if settings.openai_api_key:
        return OpenAIEmbeddings(model="text-embedding-3-large", api_key=settings.openai_api_key)
    return HuggingFaceEmbeddings(model_name=settings.embedding_model)
