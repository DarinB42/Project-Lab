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

    case_number = input("Case number: ").strip()
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

def main():
    while True:
        print("\n=== ParaSci Archive ===")
        print("1. View Research Cases")
        print("2. Create Research Case")
        print("3. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            view_cases()
        elif choice == "2":
            create_case()
        elif choice == "3":
            print("Exiting ParaSci Archive.")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()

