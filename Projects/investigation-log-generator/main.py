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

def fetch_all_investigations(database_folder):
    database_path = database_folder / "investigations.db"

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT case_number, location, investigation_date, weather, evidence_type
        FROM investigations
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
        ORDER BY generated_on DESC
    """, (f"%{location_search}%",))

    results = cursor.fetchall()
    connection.close()

    display_investigations(results)

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

    while True:
        print("\nInvestigation Log Generator")
        print("---------------------------")
        print("1. Create new investigation")
        print("2. View all investigations")
        print("3. Search by evidence type")
        print("4. Search by location")
        print("5. Exit")

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
            print("Goodbye.")
            break
        else:
            print("Please select a valid option.")

if __name__ == "__main__":
    main()
    