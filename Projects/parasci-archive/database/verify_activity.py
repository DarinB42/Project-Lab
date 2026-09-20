from database_service import get_connection

with get_connection() as connection:
    rows = connection.execute(
        """
        SELECT
            rc.case_number,
            rc.case_name,
            ra.activity_number,
            ra.activity_name,
            ra.activity_status,
            o.organization_name,
            ao.organization_role,
            l.location_code,
            l.location_name
        FROM research_case AS rc
        JOIN case_activity AS ca
            ON ca.case_id = rc.case_id
        JOIN research_activity AS ra
            ON ra.activity_id = ca.activity_id
        JOIN activity_organization AS ao
            ON ao.activity_id = ra.activity_id
        JOIN organization AS o
            ON o.organization_id = ao.organization_id
        JOIN activity_location AS al
            ON al.activity_id = ra.activity_id
        JOIN location AS l
            ON l.location_id = al.location_id
        WHERE rc.case_number = ?
        ORDER BY ra.activity_number, o.organization_name, l.location_name
        """,
        ("AHF-001",),
    ).fetchall()

if not rows:
    print("No complete Case–Activity–Organization–Location connection found.")
else:
    for row in rows:
        print(f"Case: {row['case_number']} — {row['case_name']}")
        print(f"Activity: {row['activity_number']} — {row['activity_name']}")
        print(f"Status: {row['activity_status']}")
        print(
            f"Organization: {row['organization_name']} "
            f"({row['organization_role']})"
        )
        print(f"Location: {row['location_code']} — {row['location_name']}")

print("\nActivity participants:")

with get_connection() as connection:
    participants = connection.execute(
        """
        SELECT
            p.display_name,
            ap.participation_role
        FROM research_activity AS ra
        JOIN activity_person AS ap
            ON ap.activity_id = ra.activity_id
        JOIN person AS p
            ON p.person_id = ap.person_id
        WHERE ra.activity_number = ?
        ORDER BY p.display_name
        """,
        ("INV-AHF-001",),
    ).fetchall()

if not participants:
    print("No participants found.")
else:
    for participant in participants:
        print(
            f"  {participant['display_name']} "
            f"— {participant['participation_role']}"
        )

