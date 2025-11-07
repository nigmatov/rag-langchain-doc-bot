# rag-langchain-doc-bot
RAG demo with LangChain, Chroma, and Streamlit. Ingest PDFs or text, ask questions, view sources. Optional RAGAS eval.

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
