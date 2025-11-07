from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from .embedder import get_embedding_fn
from .settings import settings

_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)

def _load_paths(paths):
    docs = []
    for p in paths:
        if p.lower().endswith(".pdf"):
            docs.extend(PyPDFLoader(p).load())
        else:
            docs.extend(TextLoader(p, encoding="utf-8").load())
    return docs

def get_store():
    emb = get_embedding_fn()
    store = Chroma(collection_name=settings.collection_name, embedding_function=emb, persist_directory=settings.persist_dir)
    return store

def ingest_files(paths):
    docs = _load_paths(paths)
    splits = _splitter.split_documents(docs)
    store = get_store()
    store.add_documents(splits)
    store.persist()
    return len(splits)
