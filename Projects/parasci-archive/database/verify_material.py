from database_service import get_connection

with get_connection() as connection:
    rows = connection.execute(
        """
        SELECT
            ra.activity_number,
            re.event_type,
            re.event_start,
            rm.material_number,
            rm.material_name,
            rm.material_type,
            rm.file_path
        FROM research_activity AS ra
        JOIN research_event AS re
            ON re.activity_id = ra.activity_id
        JOIN event_material AS em
            ON em.event_id = re.event_id
        JOIN research_material AS rm
            ON rm.material_id = em.material_id
        WHERE ra.activity_number = ?
          AND rm.material_number = ?
        """,
        ("INV-AHF-001", "MAT-AHF-001"),
    ).fetchall()

if not rows:
    print("No Event–Material connection found.")
else:
    for row in rows:
        print(f"Activity: {row['activity_number']}")
        print(f"Event: {row['event_type']}")
        print(f"Event start: {row['event_start']}")
        print(f"Material number: {row['material_number']}")
        print(f"Material name: {row['material_name']}")
        print(f"Material type: {row['material_type']}")
        print(f"File path: {row['file_path'] or 'No file registered'}")

