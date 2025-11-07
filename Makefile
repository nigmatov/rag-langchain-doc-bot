.PHONY: setup api ui eval
setup:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

api:
	uvicorn app.api:app --reload --port 8000

ui:
	streamlit run ui/streamlit_app.py

eval:
	python app/evaluator.py
