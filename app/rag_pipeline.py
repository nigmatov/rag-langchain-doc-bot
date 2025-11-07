import time
from langchain_community.llms import OpenAI as LegacyOpenAI  # optional legacy
from langchain_openai import ChatOpenAI
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from .settings import settings
from .embedder import get_embedding_fn
from .index_store import get_store

SYSTEM_PROMPT = "You are a concise assistant. Use the provided context only. If unsure, say 'I don't know'."

def _get_llm():
    if settings.openai_api_key:
        return ChatOpenAI(model=settings.llm_model, api_key=settings.openai_api_key, temperature=0)
    class Dummy:
        def invoke(self, prompt):
            return type("Obj", (), {"content": "Local mode: No LLM key set. Showing similar context snippets."})
    return Dummy()

def ask_question(q: str, k: int = 4):
    start = time.time()
    store = get_store()
    emb = get_embedding_fn()  # ensures embeddings are initialized
    vec_retr = store.as_retriever(search_kwargs={"k": k})
    # build BM25 corpus from stored documents (best-effort; may be empty on first run)
    try:
        texts = [d for d in store._collection.get(include=["documents"])["documents"]]
    except Exception:
        texts = []
    bm25 = BM25Retriever.from_texts(texts or [""])
    bm25.k = k
    retriever = EnsembleRetriever(retrievers=[vec_retr, bm25], weights=[0.65, 0.35])
    docs = retriever.get_relevant_documents(q)
    context = "\n\n".join([d.page_content[:1200] for d in docs])
    meta = [{"source": (d.metadata.get("source") or d.metadata.get("file_path") or "unknown"),
             "page": d.metadata.get("page", 0)} for d in docs]

    llm = _get_llm()
    try:
        prompt = f"{SYSTEM_PROMPT}\n\nContext:\n{context}\n\nQuestion: {q}\nAnswer:"
        out = llm.invoke(prompt)
        answer = getattr(out, "content", str(out))
    except Exception:
        answer = "Failed to call LLM. Showing top context."
    latency = int((time.time() - start) * 1000)
    return {"answer": answer, "sources": meta, "latency_ms": latency}
