import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).parent.parent / "data" / "database.db"


def get_connection(database_path=DATABASE_PATH):
    database_path = Path(database_path)

    database_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(database_path)

    connection.row_factory = sqlite3.Row

    return connection


def init_database(database_path=DATABASE_PATH):
    connection = get_connection(database_path)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()