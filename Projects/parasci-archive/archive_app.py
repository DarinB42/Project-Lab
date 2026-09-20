from database.database_service import get_connection

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


def main():
    while True:
        print("\n=== ParaSci Archive ===")
        print("1. View Research Cases")
        print("2. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            view_cases()
        elif choice == "2":
            print("Exiting ParaSci Archive.")
            break
        else:
            print("Invalid option. Please choose 1 or 2.")


if __name__ == "__main__":
    main()

