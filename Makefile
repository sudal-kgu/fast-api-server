VENV := .venv
PYTHON := $(VENV)/bin/python
UVICORN := $(VENV)/bin/uvicorn

.PHONY: install run dev

install:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

run:
	$(UVICORN) main:app --host 0.0.0.0 --port 8000

dev:
	$(UVICORN) main:app --host 0.0.0.0 --port 8000 --reload