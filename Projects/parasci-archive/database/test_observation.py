from database_service import get_connection

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
        raise ValueError("Ashford House Activity was not found.")

    # Reuse the fictional test event if it already exists.
    event = connection.execute(
        """
        SELECT event_id
        FROM research_event
        WHERE activity_id = ?
          AND event_type = ?
          AND event_start = ?
        """,
        (
            activity["activity_id"],
            "Audio Recording Session",
            "2026-09-20 20:00:00",
        ),
    ).fetchone()

    if event is None:
        cursor = connection.execute(
            """
            INSERT INTO research_event (
                activity_id,
                event_type,
                event_start,
                event_end,
                event_description
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                activity["activity_id"],
                "Audio Recording Session",
                "2026-09-20 20:00:00",
                "2026-09-20 20:20:00",
                "Fictional test recording session at Ashford House.",
            ),
        )
        event_id = cursor.lastrowid
    else:
        event_id = event["event_id"]

    # Reuse the fictional observation if it already exists.
    observation = connection.execute(
        """
        SELECT observation_id
        FROM observation
        WHERE event_id = ?
          AND observed_at = ?
          AND description = ?
        """,
        (
            event_id,
            "2026-09-20 20:07:00",
            "Three faint tapping sounds were heard during the recording session.",
        ),
    ).fetchone()

    if observation is None:
        connection.execute(
            """
            INSERT INTO observation (
                event_id,
                observed_at,
                observation_type,
                description
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                event_id,
                "2026-09-20 20:07:00",
                "Auditory",
                "Three faint tapping sounds were heard during the recording session.",
            ),
        )

with get_connection() as connection:
    investigator = connection.execute(
        """
        SELECT p.person_id
        FROM person AS p
        JOIN activity_person AS ap
            ON ap.person_id = p.person_id
        JOIN research_activity AS ra
            ON ra.activity_id = ap.activity_id
        WHERE ra.activity_number = ?
          AND p.display_name = ?
        """,
        ("INV-AHF-001", "Alex Morgan"),
    ).fetchone()

    if investigator is None:
        raise ValueError("Alex Morgan's activity assignment was not found.")

    connection.execute(
        """
        UPDATE observation
        SET recorded_by_person_id = ?
        WHERE event_id = ?
          AND observed_at = ?
          AND description = ?
        """,
        (
            investigator["person_id"],
            event_id,
            "2026-09-20 20:07:00",
            "Three faint tapping sounds were heard during the recording session.",
        ),
    )
    
print("Fictional research event and observation confirmed.")

