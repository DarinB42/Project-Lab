from database_service import get_connection

MATERIAL_NUMBER = "MAT-AHF-001"

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
        raise ValueError("Ashford House recording Event was not found.")

    # Register the fictional recording if it does not already exist.
    connection.execute(
        """
        INSERT INTO research_material (
            activity_id,
            material_number,
            material_type,
            material_name,
            description
        )
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(material_number) DO NOTHING
        """,
        (
            activity["activity_id"],
            MATERIAL_NUMBER,
            "Audio",
            "Ashford House Test Recording",
            "Fictional audio material for testing database relationships.",
        ),
    )

    material = connection.execute(
        """
        SELECT material_id, activity_id
        FROM research_material
        WHERE material_number = ?
        """,
        (MATERIAL_NUMBER,),
    ).fetchone()

    if material["activity_id"] != activity["activity_id"]:
        raise ValueError("The material belongs to a different Activity.")

    # Connect the recording to the Event it documents.
    connection.execute(
        """
        INSERT INTO event_material (event_id, material_id)
        VALUES (?, ?)
        ON CONFLICT(event_id, material_id) DO NOTHING
        """,
        (event["event_id"], material["material_id"]),
    )

print("Fictional audio material registered and linked to its Event.")

