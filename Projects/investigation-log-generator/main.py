from datetime import datetime
from pathlib import Path
import json
import sqlite3


def ask_question(prompt):
    return input(prompt + " ")


def choose_option(prompt, options):
    print(f"\n{prompt}")

    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    while True:
        choice = input("Select option number: ")

        if not choice.isdigit():
            print("Please enter a number.")
            continue

        choice = int(choice)

        if 1 <= choice <= len(options):
            return options[choice - 1]

        print(f"Please enter a number between 1 and {len(options)}.")

def generate_case_id(data_folder):
    today = datetime.now().strftime("%Y-%m-%d")
    existing_files = list(data_folder.glob(f"{today}-*_data.json"))

    next_number = len(existing_files) + 1

    return f"{today}-{next_number:03d}"

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
            generated_on TEXT
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
            generated_on
            archived INTEGER DEFAULT
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
    ))

    connection.commit()
    connection.close()

def ensure_database_schema(database_folder):
    database_path = database_folder / "investigations.db"

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

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

def display_investigations(investigations):
    if not investigations:
        print("\nNo investigations found.")
        return

    print("\nInvestigations:")
    print("----------------")

    for case_number, location, investigation_date, weather, evidence_type in investigations:
        print(f"Case: {case_number}")
        print(f"Location: {location}")
        print(f"Date: {investigation_date}")
        print(f"Weather: {weather}")
        print(f"Evidence Type: {evidence_type}")
        print("----------------")

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

    display_investigations(results)

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

    display_investigations(results)

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
        print("\nNo investigation found with that Case ID.")
        return

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

    print("\nFull Investigation Details")
    print("--------------------------")
    print(f"Case Number: {case_number}")
    print(f"Location: {location}")
    print(f"Investigation Date: {investigation_date}")
    print(f"Investigators: {investigators}")
    print(f"Weather: {weather}")
    print(f"Evidence Type: {evidence_type}")
    print(f"Reported Activity: {reported_activity}")
    print(f"Equipment Used: {equipment_used}")
    print(f"Observations: {observations}")
    print(f"Initial Conclusion: {initial_conclusion}")
    print(f"Generated On: {generated_on}")

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
        print("\nNo investigation found with that Case ID.")
        return

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
        print("Invalid selection.")
        return

    cursor.execute(f"""
        UPDATE investigations
        SET {field_name} = ?
        WHERE case_number = ?
    """, (new_value, case_number))

    connection.commit()
    connection.close()

    print("\nInvestigation updated successfully.")

def archive_investigation(database_folder):
    case_number = ask_question("Enter Case ID to archive:")

    database_path = database_folder / "investigations.db"

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT case_number
        FROM investigations
        WHERE case_number = ?
        AND archived = 0
    """, (case_number,))

    result = cursor.fetchone()

    if result is None:
        connection.close()
        print("\nNo active investigation found with that Case ID.")
        return

    confirm = ask_question(
        "Are you sure you want to archive this investigation? Type YES to confirm:"
    )

    if confirm != "YES":
        connection.close()
        print("Archive cancelled.")
        return

    cursor.execute("""
        UPDATE investigations
        SET archived = 1
        WHERE case_number = ?
    """, (case_number,))

    connection.commit()
    connection.close()

    print("\nInvestigation archived successfully.")

def create_new_investigation():
    print("Investigation Log Generator")
    print("---------------------------")

    generated_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logs_folder = Path("logs")
    data_folder = Path("data")
    database_folder = Path("database")

    logs_folder.mkdir(exist_ok=True)
    data_folder.mkdir(exist_ok=True)
    database_folder.mkdir(exist_ok=True)

    case_number = generate_case_id(data_folder)
    print(f"Generated Case ID: {case_number}")

    location = ask_question("Location:")
    investigation_date = ask_question("Investigation date:")
    investigators = ask_question("Investigators:")

    weather = choose_option(
        "Weather conditions:",
        ["Clear", "Cloudy", "Rain", "Storm", "Fog", "Other"]
    )

    evidence_type = choose_option(
        "Type of activity observed:",
        ["Visual", "Audio", "Physical", "Environmental", "None", "Other"]
    )

    reported_activity = ask_question("Reported activity:")
    equipment_used = ask_question("Equipment used:")
    observations = ask_question("Observations:")
    initial_conclusion = ask_question("Initial conclusion:")

    investigation = {
        "case_number": case_number,
        "location": location,
        "investigation_date": investigation_date,
        "investigators": investigators,
        "weather": weather,
        "evidence_type": evidence_type,
        "reported_activity": reported_activity,
        "equipment_used": equipment_used,
        "observations": observations,
        "initial_conclusion": initial_conclusion,
        "generated_on": generated_on,
    }

    log_text = f"""
# Investigation Log

## Case Information
Case Number: {investigation["case_number"]}
Location: {investigation["location"]}
Investigation Date: {investigation["investigation_date"]}
Investigators: {investigation["investigators"]}

## Conditions
Weather/Conditions: {investigation["weather"]}

## Evidence Type
{investigation["evidence_type"]}

## Reported Activity
{investigation["reported_activity"]}

## Equipment Used
{investigation["equipment_used"]}

## Observations
{investigation["observations"]}

## Initial Conclusion
{investigation["initial_conclusion"]}

Generated On: {investigation["generated_on"]}
"""


    safe_case_number = investigation["case_number"].replace(" ", "_")

    log_path = logs_folder / f"{safe_case_number}_log.md"
    data_path = data_folder / f"{safe_case_number}_data.json"

    log_path.write_text(log_text, encoding="utf-8")

    data_path.write_text(
        json.dumps(investigation, indent=4),
        encoding="utf-8"
    )

    save_to_database(investigation, database_folder)

    print(f"\nMarkdown log created: {log_path}")
    print(f"JSON data created: {data_path}")
    print("Investigation saved to SQLite database.")

def main():
    database_folder = Path("database")
    database_folder.mkdir(exist_ok=True)
    ensure_database_schema(database_folder)

    while True:
        print("\nInvestigation Log Generator")
        print("---------------------------")
        print("1. Create new investigation")
        print("2. View all investigations")
        print("3. Search by evidence type")
        print("4. Search by location")
        print("5. View investigation details")
        print("6. Edit investigation")
        print("7. Archive investigation")
        print("8. Exit")

        choice = input("Select option number: ")

        if choice == "1":
            create_new_investigation()
        elif choice == "2":
            investigations = fetch_all_investigations(database_folder)
            display_investigations(investigations)
        elif choice == "3":
            search_by_evidence_type(database_folder)
        elif choice == "4":
            search_by_location(database_folder)
        elif choice == "5":
            view_investigation_details(database_folder)
        elif choice == "6":
            edit_investigation(database_folder)
        elif choice == "7":
            archive_investigation(database_folder)
        elif choice == "8":
            print("Goodbye.")
            return
        else:
            print("Please select a valid option.")
            
if __name__ == "__main__":
    main()
    