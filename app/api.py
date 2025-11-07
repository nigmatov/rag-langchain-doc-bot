from fastapi import FastAPI, UploadFile
from .index_store import ingest_files
from .rag_pipeline import ask_question

app = FastAPI()

@app.post("/ingest")
async def ingest(files: list[UploadFile]):
    paths = []
    for f in files:
        p = f"/tmp/{f.filename}"
        with open(p, "wb") as w:
            w.write(await f.read())
        paths.append(p)
    n = ingest_files(paths)
    return {"indexed_chunks": n}

@app.get("/ask")
def ask(q: str, k: int = 4):
    return ask_question(q, k=k)

@app.get("/health")
def health():
    return {"ok": True}
