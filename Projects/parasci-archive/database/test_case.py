
import sqlite3
from pathlib import Path

DATABASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = DATABASE_DIR / "parasci_archive.db"
TEST_SQL_PATH = DATABASE_DIR / "test_case.sql"


def test_case():
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON;")

        # Create the test Case if it does not already exist.
        existing_case = connection.execute(
            """
            SELECT case_id
            FROM research_case
            WHERE case_number = ?;
            """,
            ("AHF-001",),
        ).fetchone()

        
        if existing_case is None:
            print("ERROR: Ashford House Case does not exist.")
            print("The Case must be created before linking its Location.")
            return

        # Create the Location if it does not already exist.
        connection.execute(
            """
            INSERT OR IGNORE INTO location (
                location_code,
                location_name,
                location_type,
                description
            )
            VALUES (?, ?, ?, ?);
            """,
            (
                "AHF",
                "Ashford House",
                "Residential Property",
                "Fictional historic residential property used for ParaSci prototype testing.",
            ),
        )

        # Connect the existing Case to its Location.
        connection.execute(
            """
            INSERT OR IGNORE INTO case_location (
                case_id,
                location_id,
                relationship_role
            )
            SELECT
                c.case_id,
                l.location_id,
                ?
            FROM research_case AS c
            CROSS JOIN location AS l
            WHERE c.case_number = ?
              AND l.location_code = ?;
            """,
            ("Primary", "AHF-001", "AHF"),
        )

        print("Ashford House Location and Case relationship verified.")

        # Retrieve the Case and its related reference data.
        case = connection.execute(
            """
            SELECT
                c.case_id,
                c.case_number,
                c.case_name,
                d.domain_name,
                s.status_name,
                c.opened_date
            FROM research_case AS c
            JOIN domain AS d
                ON c.primary_domain_id = d.domain_id
            JOIN case_status AS s
                ON c.case_status_id = s.case_status_id
            WHERE c.case_number = ?;
            """,
            ("AHF-001",),
        ).fetchone()

    if case is None:
        print("ERROR: Ashford House Case was not found.")
        return

    print("\nParaSci Research Case")
    print("---------------------")
    print(f"Internal ID: {case[0]}")
    print(f"Case Number: {case[1]}")
    print(f"Case Name: {case[2]}")
    print(f"Primary Domain: {case[3]}")
    print(f"Case Status: {case[4]}")
    print(f"Opened Date: {case[5]}")

    # Retrieve all Locations associated with this Case.
    with sqlite3.connect(DATABASE_PATH) as connection:
        locations = connection.execute(
            """
            SELECT
                l.location_code,
                l.location_name,
                cl.relationship_role
            FROM research_case AS c
            JOIN case_location AS cl
                ON c.case_id = cl.case_id
            JOIN location AS l
                ON cl.location_id = l.location_id
            WHERE c.case_number = ?
            ORDER BY l.location_name;
            """,
            ("AHF-001",),
        ).fetchall()

    print("\nAssociated Locations:")
    for location_code, location_name, relationship_role in locations:
        print(
            f"  {location_code}: {location_name} "
            f"({relationship_role})"
        )


if __name__ == "__main__":
    test_case()
