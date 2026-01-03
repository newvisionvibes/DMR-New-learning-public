"""
db.py - Minimal Postgres helper for the ETF RS Analyzer project.

Provides: get_connection, fetch_one, fetch_all, execute.

Uses DATABASE_URL from config.py or the DATABASE_URL environment
variable (Fly.io secret in production).
"""

import os
from typing import Any, Dict, Iterable, List, Optional

import psycopg2
from psycopg2.extras import RealDictCursor

from config import DATABASE_URL as DEFAULT_DATABASE_URL


def _get_db_url() -> str:
    """
    Return DATABASE_URL, preferring environment variable over config.
    """
    env_url = os.getenv("DATABASE_URL")
    return env_url or DEFAULT_DATABASE_URL


def get_connection():
    """
    Open a new autocommit connection with RealDictCursor so that
    rows are returned as dicts instead of tuples.
    """
    url = _get_db_url()
    conn = psycopg2.connect(url, cursor_factory=RealDictCursor)
    conn.autocommit = True
    return conn


def fetch_one(query: str, params: Optional[Iterable[Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Execute a SELECT and return a single row (or None).
    """
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(query, params or ())
        return cur.fetchone()


def fetch_all(query: str, params: Optional[Iterable[Any]] = None) -> List[Dict[str, Any]]:
    """
    Execute a SELECT and return all rows as a list of dicts.
    """
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(query, params or ())
        return cur.fetchall()


def execute(query: str, params: Optional[Iterable[Any]] = None) -> None:
    """
    Execute an INSERT/UPDATE/DELETE statement.
    """
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(query, params or ())
