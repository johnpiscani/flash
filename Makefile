# AI Agent Management Platform - Makefile

.PHONY: help install run backend frontend clean test setup-test

help:
	@echo "AI Agent Management Platform"
	@echo "Available commands:"
	@echo "  install      - Install dependencies"
	@echo "  run          - Run both backend and frontend"
	@echo "  backend      - Run only FastAPI backend"
	@echo "  frontend     - Run only Streamlit frontend"
	@echo "  clean        - Clean up cache files"
	@echo "  test         - Run backend tests"
	@echo "  setup-test   - Test project setup and imports"

install:
	pip install -r requirements.txt

run:
	python launch.py

backend:
	python main.py

frontend:
	streamlit run app/streamlit_app.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test:
	python test_backend.py

setup-test:
	python test_setup.py