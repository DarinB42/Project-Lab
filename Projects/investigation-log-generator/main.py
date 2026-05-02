from datetime import datetime
from pathlib import Path


def ask_question(prompt):
    return input(prompt + " ")


def main():
    print("Investigation Log Generator")
    print("---------------------------")

    case_number = ask_question("Case number:")
    location = ask_question("Location:")
    investigation_date = ask_question("Investigation date:")
    investigators = ask_question("Investigators:")
    weather = ask_question("Weather/conditions:")
    reported_activity = ask_question("Reported activity:")
    equipment_used = ask_question("Equipment used:")
    observations = ask_question("Observations:")
    conclusion = ask_question("Initial conclusion:")

    log_text = f"""
# Investigation Log

## Case Information
Case Number: {case_number}
Location: {location}
Investigation Date: {investigation_date}
Investigators: {investigators}

## Conditions
Weather/Conditions: {weather}

## Reported Activity
{reported_activity}

## Equipment Used
{equipment_used}

## Observations
{observations}

## Initial Conclusion
{conclusion}

Generated On: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

    logs_folder = Path("logs")
    logs_folder.mkdir(exist_ok=True)

    filename = f"{case_number.replace(' ', '_')}_log.md"
    file_path = logs_folder / filename

    file_path.write_text(log_text, encoding="utf-8")

    print(f"\nLog created successfully: {file_path}")


if __name__ == "__main__":
    main()