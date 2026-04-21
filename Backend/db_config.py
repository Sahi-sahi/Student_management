# ============================================================
#  db_config.py  —  Database Connection Manager
# ============================================================

import mysql.connector
from mysql.connector import Error
import os

DB_CONFIG = {
    "host":     os.environ.get("DB_HOST", "localhost"),
    "port":     int(os.environ.get("DB_PORT", 3306)),
    "user":     os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),   # ← change this
    "database": os.environ.get("DB_NAME", "myproject_db"),
    "autocommit": True,
    "charset":  "utf8mb4",
}


def get_connection():
    """Return a live MySQL connection, raise RuntimeError on failure."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        raise RuntimeError(f"Database connection failed: {e}")


def get_cursor(conn):
    """Return a dict cursor for the given connection."""
    return conn.cursor(dictionary=True)
