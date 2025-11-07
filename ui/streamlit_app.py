import streamlit as st
import requests

st.set_page_config(page_title="RAG Bot", layout="wide")
st.title("RAG Doc Bot")

with st.sidebar:
    st.header("Ingest")
    files = st.file_uploader("Upload PDFs or text", accept_multiple_files=True, type=["pdf","txt","md"])
    if st.button("Index") and files:
        fs = [("files", (f.name, f.getvalue(), "application/octet-stream")) for f in files]
        r = requests.post("http://localhost:8000/ingest", files=fs)
        st.write(r.json())

q = st.text_input("Ask a question:")
if st.button("Ask") and q:
    r = requests.get("http://localhost:8000/ask", params={"q": q, "k": 4})
    data = r.json()
    st.subheader("Answer")
    st.write(data.get("answer"))
    st.subheader("Sources")
    st.json(data.get("sources"))
    st.caption(f"Latency: {data.get('latency_ms')} ms")
