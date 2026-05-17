def display_investigations(investigations):
    if not investigations:
        print("\nNo investigations found.")
        return

    print("\nInvestigations:")
    print("----------------")

    for case_number, location, investigation_date, weather, evidence_type in investigations:
        print(f"Case: {case_number}")
        print(f"Location: {location}")
        print(f"Date: {investigation_date}")
        print(f"Weather: {weather}")
        print(f"Evidence Type: {evidence_type}")
        print("----------------")

def display_investigation_details(result):
    if result is None:
        print("\nNo investigation found with that Case ID.")
        return

    (
        case_number,
        location,
        investigation_date,
        investigators,
        weather,
        evidence_type,
        reported_activity,
        equipment_used,
        observations,
        initial_conclusion,
        generated_on,
    ) = result

    print("\nFull Investigation Details")
    print("--------------------------")
    print(f"Case Number: {case_number}")
    print(f"Location: {location}")
    print(f"Investigation Date: {investigation_date}")
    print(f"Investigators: {investigators}")
    print(f"Weather: {weather}")
    print(f"Evidence Type: {evidence_type}")
    print(f"Reported Activity: {reported_activity}")
    print(f"Equipment Used: {equipment_used}")
    print(f"Observations: {observations}")
    print(f"Initial Conclusion: {initial_conclusion}")
    print(f"Generated On: {generated_on}")