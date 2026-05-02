from datetime import datetime
from pathlib import Path
import json


def ask_question(prompt):
    return input(prompt + " ")


def main():
    print("Investigation Log Generator")
    print("---------------------------")

    generated_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    investigation = {
        "case_number": ask_question("Case number:"),
        "location": ask_question("Location:"),
        "investigation_date": ask_question("Investigation date:"),
        "investigators": ask_question("Investigators:"),
        "weather": ask_question("Weather/conditions:"),
        "reported_activity": ask_question("Reported activity:"),
        "equipment_used": ask_question("Equipment used:"),
        "observations": ask_question("Observations:"),
        "initial_conclusion": ask_question("Initial conclusion:"),
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

    logs_folder = Path("logs")
    data_folder = Path("data")

    logs_folder.mkdir(exist_ok=True)
    data_folder.mkdir(exist_ok=True)

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
    