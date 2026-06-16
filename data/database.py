# data/database.py
"""Database connection helper.
Supports SQLite (default) and MySQL based on configuration.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from .config import DB_TYPE, SQLITE_DB_PATH, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

_engine: Engine | None = None

def get_engine() -> Engine:
    """Create and cache a SQLAlchemy engine based on DB_TYPE.
    Returns:
        Engine: SQLAlchemy engine instance.
    """
    global _engine
    if _engine is not None:
        return _engine
    if DB_TYPE == "sqlite":
        conn_str = f"sqlite:///{SQLITE_DB_PATH}"
    elif DB_TYPE == "mysql":
        conn_str = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
        )
    else:
        raise ValueError(f"Unsupported DB_TYPE: {DB_TYPE}")
    _engine = create_engine(conn_str, echo=False, future=True)
    return _engine

def get_connection():
    """Convenient wrapper returning a DB-API connection.
    Usage:
        conn = get_connection()
        # use conn.execute(...)
        conn.close()
    """
    engine = get_engine()
    return engine.connect()
