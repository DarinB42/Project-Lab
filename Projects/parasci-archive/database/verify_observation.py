from database_service import get_connection

with get_connection() as connection:
    rows = connection.execute(
        """
        SELECT
            ra.activity_number,
            re.event_type,
            re.event_start,
            re.event_end,
            o.observed_at,
            o.observation_type,
            o.description
        FROM research_activity AS ra
        JOIN research_event AS re
            ON re.activity_id = ra.activity_id
        JOIN observation AS o
            ON o.event_id = re.event_id
        WHERE ra.activity_number = ?
        ORDER BY re.event_start, o.observed_at
        """,
        ("INV-AHF-001",),
    ).fetchall()

if not rows:
    print("No linked events and observations found.")
else:
    for row in rows:
        print(f"Activity: {row['activity_number']}")
        print(f"Event: {row['event_type']}")
        print(f"Event start: {row['event_start']}")
        print(f"Event end: {row['event_end']}")
        print(f"Observation time: {row['observed_at']}")
        print(f"Observation type: {row['observation_type']}")
        print(f"Description: {row['description']}")

print("\nObservation recorder:")

with get_connection() as connection:
    recorder = connection.execute(
        """
        SELECT
            p.display_name,
            o.observed_at,
            o.description
        FROM observation AS o
        JOIN person AS p
            ON p.person_id = o.recorded_by_person_id
        JOIN research_event AS re
            ON re.event_id = o.event_id
        JOIN research_activity AS ra
            ON ra.activity_id = re.activity_id
        WHERE ra.activity_number = ?
          AND o.observed_at = ?
        """,
        ("INV-AHF-001", "2026-09-20 20:07:00"),
    ).fetchone()

if recorder is None:
    print("No recorder found for the test observation.")
else:
    print(f"Recorded by: {recorder['display_name']}")
    print(f"Observation time: {recorder['observed_at']}")
    print(f"Description: {recorder['description']}")

