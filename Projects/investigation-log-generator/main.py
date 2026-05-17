from datetime import datetime
from pathlib import Path
import json
import sqlite3

from services.database_service import (
    save_to_database,
    ensure_database_schema,
    fetch_all_investigations,
    search_by_evidence_type,
    search_by_location,
    view_investigation_details,
    edit_investigation
    )

from utils.helpers import ask_question, choose_option, generate_case_id

BASE_DIR = Path(__file__).resolve().parent

from services.database_service import (
    save_to_database,
    ensure_database_schema,
    fetch_all_investigations
)

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

    logs_folder = BASE_DIR / "logs"
    data_folder = BASE_DIR / "data"
    database_folder = BASE_DIR / "database"   

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
    database_folder = BASE_DIR / "database"
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
            results = search_by_evidence_type(database_folder)
            display_investigations(results)
        elif choice == "4":
            results = search_by_location(database_folder)
            display_investigations(results)
        elif choice == "5":
            result = view_investigation_details(database_folder)
            if result is None:
                print("\nNo investigation found with that Case ID.")
            else:
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
        elif choice == "6":
            message = edit_investigation(database_folder)
            print(f"\n{message}")    
        elif choice == "7":
            archive_investigation(database_folder)
        elif choice == "8":
            print("Goodbye.")
            return
        else:
            print("Please select a valid option.")
            
if __name__ == "__main__":
    main()
    