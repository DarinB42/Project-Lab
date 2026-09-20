
from database_service import get_connection

with get_connection() as connection:
    # Create or reuse the fictional research organization.
    connection.execute(
        """
        INSERT OR IGNORE INTO organization (
            organization_name,
            short_name,
            organization_type
        )
        VALUES (?, ?, ?)
        """,
        (
            "Chesapeake Anomalous Research Group",
            "CARG",
            "Independent Research Group",
        ),
    )

    # Create or reuse the fictional Ashford House investigation.
    connection.execute(
        """
        INSERT OR IGNORE INTO research_activity (
            activity_number,
            activity_name,
            activity_type,
            activity_status,
            purpose
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            "INV-AHF-001",
            "Ashford House Field Investigation",
            "INV",
            "Planning",
            "Investigate recurring reports of footsteps, voices, and a figure.",
        ),
    )

    # Look up the existing Case and the two records above.
    case = connection.execute(
        "SELECT case_id FROM research_case WHERE case_number = ?",
        ("AHF-001",),
    ).fetchone()

    activity = connection.execute(
        "SELECT activity_id FROM research_activity WHERE activity_number = ?",
        ("INV-AHF-001",),
    ).fetchone()

    organization = connection.execute(
        "SELECT organization_id FROM organization WHERE organization_name = ?",
        ("Chesapeake Anomalous Research Group",),
    ).fetchone()

    if case is None:
        raise ValueError("Case AHF-001 was not found.")

    # Connect the Activity to the Case.
    connection.execute(
        """
        INSERT OR IGNORE INTO case_activity (case_id, activity_id)
        VALUES (?, ?)
        """,
        (case["case_id"], activity["activity_id"]),
    )

    # Record which organization leads this Activity.
    connection.execute(
        """
        INSERT OR IGNORE INTO activity_organization (
            activity_id,
            organization_id,
            organization_role
        )
        VALUES (?, ?, ?)
        """,
        (activity["activity_id"], organization["organization_id"], "Lead"),
    )

print("Ashford House test activity created and linked successfully.")

with get_connection() as connection:
    activity = connection.execute(
        """
        SELECT activity_id
        FROM research_activity
        WHERE activity_number = ?
        """,
        ("INV-AHF-001",),
    ).fetchone()

    location = connection.execute(
        """
        SELECT location_id
        FROM location
        WHERE location_code = ?
        """,
        ("AHF",),
    ).fetchone()

    if activity is None or location is None:
        raise ValueError("The Ashford House Activity or Location was not found.")

    connection.execute(
        """
        INSERT OR IGNORE INTO activity_location (
            activity_id,
            location_id
        )
        VALUES (?, ?)
        """,
        (activity["activity_id"], location["location_id"]),
    )

print("Ashford House activity linked to its location successfully.")

with get_connection() as connection:
    activity = connection.execute(
        """
        SELECT activity_id
        FROM research_activity
        WHERE activity_number = ?
        """,
        ("INV-AHF-001",),
    ).fetchone()

    if activity is None:
        raise ValueError("Activity INV-AHF-001 was not found.")

    # Reuse the fictional investigator already assigned to this Activity.
    person = connection.execute(
        """
        SELECT p.person_id
        FROM person AS p
        JOIN activity_person AS ap
            ON ap.person_id = p.person_id
        WHERE ap.activity_id = ?
          AND p.display_name = ?
        """,
        (activity["activity_id"], "Alex Morgan"),
    ).fetchone()

    if person is None:
        # Create the fictional person only if they are not already assigned.
        cursor = connection.execute(
            """
            INSERT INTO person (display_name, given_name, family_name)
            VALUES (?, ?, ?)
            """,
            ("Alex Morgan", "Alex", "Morgan"),
        )
        person_id = cursor.lastrowid

        connection.execute(
            """
            INSERT INTO activity_person (
                activity_id,
                person_id,
                participation_role
            )
            VALUES (?, ?, ?)
            """,
            (activity["activity_id"], person_id, "Investigator"),
        )

print("Fictional investigator assignment confirmed.")

