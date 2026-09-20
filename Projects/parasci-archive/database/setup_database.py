import sqlite3
from pathlib import Path

# Find the database folder, regardless of where
# the script is launched from.
DATABASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = DATABASE_DIR / "parasci_archive.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"
SEED_PATH = DATABASE_DIR / "seed_data.sql"


def setup_database():
    # Read our SQL table definitions and initial reference data.
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    seed_data = SEED_PATH.read_text(encoding="utf-8")

    # Create or open the SQLite database.
    with sqlite3.connect(DATABASE_PATH) as connection:
        # Enforce foreign-key relationships.
        connection.execute("PRAGMA foreign_keys = ON;")

        # Execute the SQL instructions in schema.sql.
        connection.executescript(schema)

        # Load the approved domains and Case statuses.
        connection.executescript(seed_data)

    print("ParaSci Archive database initialized successfully.")
    print(f"Database location: {DATABASE_PATH}")

    # Verify which tables exist in the database.
    with sqlite3.connect(DATABASE_PATH) as connection:
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name;
            """
        ).fetchall()

    print("\nDatabase tables:")
    for table in tables:
        print(f"  - {table[0]}")

    
    # Verify the approved reference data.
    with sqlite3.connect(DATABASE_PATH) as connection:
        domains = connection.execute(
            """
            SELECT domain_id, domain_name
            FROM domain
            ORDER BY domain_id;
            """
        ).fetchall()

        statuses = connection.execute(
            """
            SELECT case_status_id, status_name
            FROM case_status
            ORDER BY case_status_id;
            """
        ).fetchall()

    print("\nResearch domains:")
    for domain_id, domain_name in domains:
        print(f"  {domain_id}: {domain_name}")

    print("\nCase statuses:")
    for status_id, status_name in statuses:
        print(f"  {status_id}: {status_name}")


if __name__ == "__main__":
    setup_database()
