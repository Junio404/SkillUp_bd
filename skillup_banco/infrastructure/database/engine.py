from sqlalchemy import create_engine

DATABASE_URL = "mssql+pyodbc://user:password@server/db?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)
