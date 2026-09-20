
import sqlite3
from pathlib import Path

DATABASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = DATABASE_DIR / "parasci_archive.db"


def get_connection():
    """Open a connection to the ParaSci Archive database."""

    connection = sqlite3.connect(DATABASE_PATH)

    # Enforce relationships between database tables.
    connection.execute("PRAGMA foreign_keys = ON;")

    # Allow records to be accessed by column name.
    connection.row_factory = sqlite3.Row

    return connection
