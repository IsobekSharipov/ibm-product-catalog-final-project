# IBM Product Catalog Final Project

Python FastAPI product catalog with SQLAlchemy, CRUD endpoints, search, availability checks, and a foundation for Behave BDD and Selenium UI tests.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit http://127.0.0.1:8000/docs to explore the API.

## Test

```bash
pytest -q
```

The default database is SQLite (`products.db`). Upcoming assignment tasks will be implemented here.
