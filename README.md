# rag-langchain-doc-bot
RAG demo with LangChain, Chroma, and Streamlit. Ingest PDFs or text, ask questions, view sources. Optional RAGAS eval.

rag-langchain-doc-bot/
  ├─ app/
  │  ├─ api.py                    # FastAPI endpoints: /ingest, /ask, /health
  │  ├─ rag_pipeline.py           # Retriever+LLM chain with source citing
  │  ├─ embedder.py               # Pluggable embeddings (OpenAI or HF)
  │  ├─ index_store.py            # Chroma/FAISS wrapper
  │  ├─ evaluator.py              # RAGAS eval on held-out QAs
  │  └─ settings.py               # Pydantic config (keys, model names)
  ├─ ui/
  │  └─ streamlit_app.py          # Simple chat UI with file upload + source panel
  ├─ data/                        # sample docs (3–5 PDFs)
  ├─ requirements.txt
  ├─ Makefile
  └─ README.md


## Quickstart
```bash
make setup
make api      # FastAPI on :8000
make ui       # Streamlit on default port
```
Set `OPENAI_API_KEY` to use OpenAI. Otherwise falls back to local `sentence-transformers/all-MiniLM-L6-v2`.

## Endpoints
- POST `/ingest` files=[...] → index
- GET `/ask?q=...&k=4` → {answer, sources[], latency_ms}
