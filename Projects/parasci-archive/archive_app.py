from database.database_service import get_connection
import sqlite3

def view_activity_details(activity_number):
    with get_connection() as connection:
        activity = connection.execute(
            """
            SELECT activity_id, activity_number, activity_name
            FROM research_activity
            WHERE activity_number = ?
            """,
            (activity_number,),
        ).fetchone()

        if activity is None:
            print("\nActivity not found.")
            return

        events = connection.execute(
            """
            SELECT event_id, event_type, event_start
            FROM research_event
            WHERE activity_id = ?
            ORDER BY event_start
            """,
            (activity["activity_id"],),
        ).fetchall()

        print(
            f"\n--- {activity['activity_number']}: "
            f"{activity['activity_name']} ---"
        )

        if not events:
            print("\nNo Events recorded for this Activity.")
            return

        for event in events:
            print(
                f"\nEvent: {event['event_type']} "
                f"({event['event_start']})"
            )

            observations = connection.execute(
                """
                SELECT observed_at, observation_type, description
                FROM observation
                WHERE event_id = ?
                ORDER BY observed_at
                """,
                (event["event_id"],),
            ).fetchall()

            if not observations:
                print("  No Observations recorded.")
            else:
                for observation in observations:
                    print(
                        f"  Observation ({observation['observed_at']}): "
                        f"{observation['observation_type']}"
                    )
                    print(f"    {observation['description']}")

            materials = connection.execute(
                """
                SELECT
                    rm.material_number,
                    rm.material_name,
                    rm.material_type,
                    rm.file_path
                FROM research_material AS rm
                JOIN event_material AS em
                    ON em.material_id = rm.material_id
                WHERE em.event_id = ?
                ORDER BY rm.material_number
                """,
                (event["event_id"],),
            ).fetchall()

            print("  Research Materials:")

            if not materials:
                print("    No materials linked to this Event.")
            else:
                for material in materials:
                    print(
                        f"    {material['material_number']}: "
                        f"{material['material_name']} "
                        f"({material['material_type']})"
                    )
                    print(
                        f"      File: "
                        f"{material['file_path'] or 'No file registered'}"
                    )


def view_case_details(case_number):
    with get_connection() as connection:
        case = connection.execute(
            """
            SELECT case_id, case_number, case_name
            FROM research_case
            WHERE case_number = ?
            """,
            (case_number,),
        ).fetchone()

        if case is None:
            print("\nCase not found.")
            return

        activities = connection.execute(
            """
            SELECT
                ra.activity_number,
                ra.activity_name
            FROM research_activity AS ra
            JOIN case_activity AS ca
                ON ca.activity_id = ra.activity_id
            WHERE ca.case_id = ?
            ORDER BY ra.activity_number
            """,
            (case["case_id"],),
        ).fetchall()

    print(f"\n--- {case['case_number']}: {case['case_name']} ---")
    print("\nResearch Activities:")

    if not activities:
        print("No Research Activities linked to this Case.")
    else:
        for activity in activities:
            print(
                f"  {activity['activity_number']}: "
                f"{activity['activity_name']}"
            )

        activity_number = input(
            "\nEnter an Activity number to view details "
            "(or press Enter to return): "
        ).strip()

        if activity_number:
            view_activity_details(activity_number) 


def view_cases():
    with get_connection() as connection:
        cases = connection.execute(
            """
            SELECT case_number, case_name
            FROM research_case
            ORDER BY case_number
            """
        ).fetchall()

    print("\n--- Research Cases ---")

    if not cases:
        print("No cases have been registered.")
        return

    for case in cases:
        print(f"{case['case_number']}: {case['case_name']}")

    case_number = input(
        "\nEnter a Case number to view details "
        "(or press Enter to return): "
    ).strip()

    if case_number:
        view_case_details(case_number)

def choose_option(connection, table_name, id_column, name_column, label):
    rows = connection.execute(
        f"""
        SELECT {id_column}, {name_column}
        FROM {table_name}
        WHERE is_active = 1
        ORDER BY {name_column}
        """
    ).fetchall()

    if not rows:
        print(f"No active {label.lower()} options are available.")
        return None

    print(f"\nChoose a {label.lower()}:")

    for number, row in enumerate(rows, start=1):
        print(f"{number}. {row[name_column]}")

    while True:
        choice = input(f"{label} number (or Q to cancel): ").strip()

        if choice.lower() == "q":
            return None

        if choice.isdigit():
            selection = int(choice)

            if 1 <= selection <= len(rows):
                return rows[selection - 1][id_column]

        print("Invalid selection. Choose a number from the list or Q to cancel.")

def create_case():
    print("\n=== Create Research Case ===")
    print("Create a Case only after its research question has been reviewed and accepted.")

    while True:
        case_number = input("Case number (or Q to cancel): ").strip()

        if case_number.lower() == "q":
            print("Case creation cancelled.")
            return

        if not case_number:
            print("Case number is required.")
            continue

        with get_connection() as connection:
            existing_case = connection.execute(
                """
                SELECT case_name
                FROM research_case
                WHERE case_number = ?
                """,
                (case_number,),
            ).fetchone()

        if existing_case:
            print(
                f"Case {case_number} already exists: "
                f"{existing_case['case_name']}"
            )
            print("Enter a different Case number or Q to cancel.")
            continue

        break
    case_name = input("Case name: ").strip()
    opened_date = input("Date opened (YYYY-MM-DD): ").strip()
    if not case_number or not case_name:
        print("Case number and Case name are required. No Case was created.")
        return

    try:
        from datetime import date
        date.fromisoformat(opened_date)

        if len(opened_date) != 10 or opened_date[4] != "-" or opened_date[7] != "-":
            raise ValueError

    except ValueError:
        print("Enter a valid opened date in YYYY-MM-DD format. No Case was created.")
        return

    with get_connection() as connection:
        primary_domain_id = choose_option(
            connection,
            "domain",
            "domain_id",
            "domain_name",
            "Domain",
        )

        if primary_domain_id is None:
            print("Case creation cancelled.")
            return

        case_status_id = choose_option(
            connection,
            "case_status",
            "case_status_id",
            "status_name",
            "Case status",
        )

        if case_status_id is None:
            print("Case creation cancelled.")
            return

    print("\nOptional details — press Enter to leave any field blank.")
    summary = input("Research question / summary: ").strip()
    scope = input("Scope: ").strip()
    exclusions = input("Exclusions: ").strip()

    print("\nCase details entered:")
    print(f"  Number: {case_number}")
    print(f"  Name: {case_name}")
    print(f"  Opened: {opened_date}")
    print(f"  Summary: {summary or 'Not provided'}")
    print(f"  Scope: {scope or 'Not provided'}")
    print(f"  Exclusions: {exclusions or 'Not provided'}")
    confirmation = input("\nSave this Case? (Y/N): ").strip().lower()

    if confirmation != "y":
        print("Case creation cancelled. No Case was saved.")
        return

    try:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO research_case (
                    case_number,
                    case_name,
                    primary_domain_id,
                    opened_date,
                    case_status_id,
                    summary,
                    scope,
                    exclusions
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    case_number,
                    case_name,
                    primary_domain_id,
                    opened_date,
                    case_status_id,
                    summary or None,
                    scope or None,
                    exclusions or None,
                ),
            )

        print(f"Case {case_number} saved successfully.")

    except sqlite3.IntegrityError as error:
        print(f"Case could not be saved: {error}")

def create_activity():
    print("\n=== Create Research Activity ===")

    while True:
        activity_number = input("Activity number (or Q to cancel): ").strip()

        if activity_number.lower() == "q":
            print("Activity creation cancelled.")
            return

        if not activity_number:
            print("Activity number is required.")
            continue

        with get_connection() as connection:
            existing_activity = connection.execute(
                """
                SELECT activity_name
                FROM research_activity
                WHERE activity_number = ?
                """,
                (activity_number,),
            ).fetchone()

        if existing_activity:
            print(
                f"Activity {activity_number} already exists: "
                f"{existing_activity['activity_name']}"
            )
            print("Enter a different Activity number or Q to cancel.")
            continue

        break

    print(f"\nActivity number {activity_number} is available.")

    while True:
        activity_name = input("Activity name (or Q to cancel): ").strip()

        if activity_name.lower() == "q":
            print("Activity creation cancelled.")
            return

        if activity_name:
            break

        print("Activity name is required.")

    activity_types = {
        "1": ("INV", "Investigation"),
        "2": ("EXP", "Experiment"),
        "3": ("HIS", "Historical Research"),
        "4": ("CMP", "Comparative Research"),
        "5": ("COM", "Computational Research"),
    }

    print("\nChoose an Activity type:")
    for number, (code, name) in activity_types.items():
        print(f"{number}. {name} ({code})")

    while True:
        choice = input("Activity type number (or Q to cancel): ").strip()

        if choice.lower() == "q":
            print("Activity creation cancelled.")
            return

        if choice in activity_types:
            activity_type = activity_types[choice][0]
            break

        print("Invalid selection. Choose a number from the list or Q to cancel.")

    activity_statuses = [
        "Proposed",
        "Planning",
        "Ready",
        "In Progress",
        "On Hold",
        "Post-Research Review",
        "Completed",
        "Terminated",
    ]

    print("\nChoose an Activity status:")
    for number, status in enumerate(activity_statuses, start=1):
        print(f"{number}. {status}")

    while True:
        choice = input("Activity status number (or Q to cancel): ").strip()

        if choice.lower() == "q":
            print("Activity creation cancelled.")
            return

        if choice.isdigit() and 1 <= int(choice) <= len(activity_statuses):
            activity_status = activity_statuses[int(choice) - 1]
            break

        print("Invalid selection. Choose a number from the list or Q to cancel.")

    with get_connection() as connection:
        cases = connection.execute(
            """
            SELECT case_id, case_number, case_name
            FROM research_case
            ORDER BY case_number
            """
        ).fetchall()

    if not cases:
        print("No Research Cases are available. Create a Case first.")
        return

    print("\nChoose the Case to link to this Activity:")
    for number, case in enumerate(cases, start=1):
        print(f"{number}. {case['case_number']}: {case['case_name']}")

    while True:
        choice = input("Case number from the list (or Q to cancel): ").strip()

        if choice.lower() == "q":
            print("Activity creation cancelled.")
            return

        if choice.isdigit() and 1 <= int(choice) <= len(cases):
            selected_case = cases[int(choice) - 1]
            case_id = selected_case["case_id"]
            break

        print("Invalid selection. Choose a number from the list or Q to cancel.")

        print("\nOptional Activity details — press Enter to skip.")

    purpose = input("Purpose: ").strip()

    while True:
        planned_start_date = input(
            "Planned start date (YYYY-MM-DD, or Enter to skip): "
        ).strip()

        if not planned_start_date:
            break

        try:
            from datetime import date

            if (
                len(planned_start_date) != 10
                or date.fromisoformat(planned_start_date).isoformat()
                != planned_start_date
            ):
                raise ValueError

            break

        except ValueError:
            print("Enter a valid date in YYYY-MM-DD format, or press Enter to skip.")

    print(f"\nActivity: {activity_number} — {activity_name}")
    print(f"Type: {activity_type}")
    print(f"Status: {activity_status}")
    print(f"Purpose: {purpose or 'Not provided'}")
    print(f"Planned start: {planned_start_date or 'Not scheduled'}")
    print(
        f"Linked Case: {selected_case['case_number']} — "
        f"{selected_case['case_name']}"
    )
    confirmation = input("\nSave this Activity? (Y/N): ").strip().lower()

    if confirmation != "y":
        print("Activity creation cancelled. No Activity was saved.")
        return

    try:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO research_activity (
                    activity_number,
                    activity_name,
                    activity_type,
                    activity_status,
                    purpose,
                    planned_start_date
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    activity_number,
                    activity_name,
                    activity_type,
                    activity_status,
                    purpose or None,
                    planned_start_date or None,
                ),
            )

            activity_id = cursor.lastrowid

            connection.execute(
                """
                INSERT INTO case_activity (case_id, activity_id)
                VALUES (?, ?)
                """,
                (case_id, activity_id),
            )

        print(
            f"Activity {activity_number} saved and linked to "
            f"Case {selected_case['case_number']}."
        )

    except sqlite3.IntegrityError as error:
        print(f"Activity could not be saved: {error}")

def main():
    while True:
        print("\n=== ParaSci Archive ===")
        print("1. View Research Cases")
        print("2. Create Research Case")
        print("3. Create Research Activity")
        print("4. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            view_cases()
        elif choice == "2":
            create_case()
        elif choice == "3":
            create_activity()
        elif choice == "4":
            print("Exiting ParaSci Archive.")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()

