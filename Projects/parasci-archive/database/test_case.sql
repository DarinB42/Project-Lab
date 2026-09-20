
-- ParaSci Archive Prototype #2
-- Create our first test Case

INSERT INTO research_case (
    case_number,
    case_name,
    primary_domain_id,
    opened_date,
    case_status_id,
    summary,
    scope
)
VALUES (
    'AHF-001',
    'Ashford House Recurring Residential Reports',
    1,
    '2026-09-20',
    1,
    'Research into recurring reports of footsteps, voices, and visual experiences at Ashford House.',
    'Document reported events, investigate environmental explanations, and evaluate relevant historical claims.'
);


-- Create the Ashford House Location
INSERT INTO location (
    location_code,
    location_name,
    location_type,
    description
)
VALUES (
    'AHF',
    'Ashford House',
    'Residential Property',
    'Fictional historic residential property used for ParaSci prototype testing.'
);

-- Connect Ashford House to Case AHF-001
INSERT INTO case_location (
    case_id,
    location_id,
    relationship_role
)
SELECT
    c.case_id,
    l.location_id,
    'Primary'
FROM research_case AS c
CROSS JOIN location AS l
WHERE c.case_number = 'AHF-001'
  AND l.location_code = 'AHF';
