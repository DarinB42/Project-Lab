from datetime import datetime
from pathlib import Path
import json


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

def main():
    print("Investigation Log Generator")
    print("---------------------------")

    generated_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logs_folder = Path("logs")
    data_folder = Path("data")

    logs_folder.mkdir(exist_ok=True)
    data_folder.mkdir(exist_ok=True)

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

    print(f"\nMarkdown log created: {log_path}")
    print(f"JSON data created: {data_path}")


if __name__ == "__main__":
    main()
    