from sqlalchemy import text
from .engine import engine


def fetch_all(query: str, params: dict = {}):
    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        return [dict(row._mapping) for row in result]


def execute(query: str, params: dict = {}):
    with engine.begin() as conn:
        conn.execute(text(query), params)
