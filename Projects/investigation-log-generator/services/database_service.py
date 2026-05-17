import sqlite3

from utils.helpers import ask_question, choose_option

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

def search_by_location(database_folder):
    location_search = ask_question("Enter location search term:")

    database_path = database_folder / "investigations.db"

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT case_number, location, investigation_date, weather, evidence_type
        FROM investigations
        WHERE location LIKE ?
        AND archived = 0
        ORDER BY generated_on DESC
    """, (f"%{location_search}%",))

    results = cursor.fetchall()
    connection.close()

    return results

def view_investigation_details(database_folder):
    case_number = ask_question("Enter Case ID:")

    database_path = database_folder / "investigations.db"

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
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
            generated_on
        FROM investigations
        WHERE case_number = ?
    """, (case_number,))

    result = cursor.fetchone()
    connection.close()

    if result is None:
        return None

    (
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
    ) = result

    return result

def edit_investigation(database_folder):
    case_number = ask_question("Enter Case ID to edit:")

    database_path = database_folder / "investigations.db"

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT case_number, observations, initial_conclusion
        FROM investigations
        WHERE case_number = ?
    """, (case_number,))

    result = cursor.fetchone()

    if result is None:
        connection.close()
        return "No investigation found with that Case ID."    

    print("\nCurrent editable fields")
    print("-----------------------")
    print(f"1. Observations: {result[1]}")
    print(f"2. Initial Conclusion: {result[2]}")

    field_choice = input("Select field to edit: ").strip()

    if field_choice == "1":
        new_value = ask_question("Enter updated observations:")
        field_name = "observations"
    elif field_choice == "2":
        new_value = ask_question("Enter updated initial conclusion:")
        field_name = "initial_conclusion"
    else:
        connection.close()
        return "Invalid selection."

    cursor.execute(f"""
        UPDATE investigations
        SET {field_name} = ?
        WHERE case_number = ?
    """, (new_value, case_number))

    connection.commit()
    connection.close()

    return "Investigation updated successfully."