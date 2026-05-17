import sqlite3

from utils.helpers import choose_option

def save_to_database(investigation, database_folder):
    database_path = database_folder / "investigations.db"

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS investigations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_number TEXT UNIQUE,
            location TEXT,
            investigation_date TEXT,
            investigators TEXT,
            weather TEXT,
            evidence_type TEXT,
            reported_activity TEXT,
            equipment_used TEXT,
            observations TEXT,
            initial_conclusion TEXT,
            generated_on TEXT,
            archived INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        INSERT INTO investigations (
            case_number,
            location,
            investigation_date,
            investigators,
            weather,
            evidence_type,
            reported_activity,
            equipment_used,
            observations,
            initial_conclusion,
            generated_on,
            archived
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        investigation["case_number"],
        investigation["location"],
        investigation["investigation_date"],
        investigation["investigators"],
        investigation["weather"],
        investigation["evidence_type"],
        investigation["reported_activity"],
        investigation["equipment_used"],
        investigation["observations"],
        investigation["initial_conclusion"],
        investigation["generated_on"],
        0,
    ))

    connection.commit()
    connection.close()

def ensure_database_schema(database_folder):
    database_path = database_folder / "investigations.db"

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS investigations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_number TEXT UNIQUE,
            location TEXT,
            investigation_date TEXT,
            investigators TEXT,
            weather TEXT,
            evidence_type TEXT,
            reported_activity TEXT,
            equipment_used TEXT,
            observations TEXT,
            initial_conclusion TEXT,
            generated_on TEXT,
            archived INTEGER DEFAULT 0
        )
    """)

    cursor.execute("PRAGMA table_info(investigations)")
    columns = [column[1] for column in cursor.fetchall()]

    if "archived" not in columns:
        cursor.execute("""
            ALTER TABLE investigations
            ADD COLUMN archived INTEGER DEFAULT 0
        """)

    connection.commit()
    connection.close()

def fetch_all_investigations(database_folder):
    database_path = database_folder / "investigations.db"

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT case_number, location, investigation_date, weather, evidence_type
        FROM investigations
        WHERE archived = 0
        ORDER BY generated_on DESC
    """)

    results = cursor.fetchall()
    connection.close()

    return results

def search_by_evidence_type(database_folder):
    evidence_type = choose_option(
        "Search by evidence type:",
        ["Visual", "Audio", "Physical", "Environmental", "None", "Other"]
    )

    database_path = database_folder / "investigations.db"

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT case_number, location, investigation_date, weather, evidence_type
        FROM investigations
        WHERE evidence_type = ?
        AND archived = 0
        ORDER BY generated_on DESC
    """, (evidence_type,))

    results = cursor.fetchall()
    connection.close()

    return results
