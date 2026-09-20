
-- ParaSci Archive Prototype #2
-- Database schema

PRAGMA foreign_keys = ON;

-- Approved research domains
CREATE TABLE IF NOT EXISTS domain (
    domain_id INTEGER PRIMARY KEY,
    domain_name TEXT NOT NULL UNIQUE,
    description TEXT,
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1))
);

-- Approved Case statuses
CREATE TABLE IF NOT EXISTS case_status (
    case_status_id INTEGER PRIMARY KEY,
    status_name TEXT NOT NULL UNIQUE,
    description TEXT,
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1))
);

-- ParaSci research Cases
CREATE TABLE IF NOT EXISTS research_case (
    case_id INTEGER PRIMARY KEY,
    case_number TEXT NOT NULL UNIQUE,
    case_name TEXT NOT NULL,
    primary_domain_id INTEGER NOT NULL,
    opened_date TEXT NOT NULL,
    case_status_id INTEGER NOT NULL,
    summary TEXT,
    scope TEXT,
    exclusions TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (primary_domain_id)
        REFERENCES domain(domain_id),

    FOREIGN KEY (case_status_id)
        REFERENCES case_status(case_status_id)
);


-- Reusable research locations
CREATE TABLE IF NOT EXISTS location (
    location_id INTEGER PRIMARY KEY,
    location_code TEXT NOT NULL UNIQUE,
    location_name TEXT NOT NULL,
    location_type TEXT,
    description TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Connect Cases to Locations
CREATE TABLE IF NOT EXISTS case_location (
    case_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    relationship_role TEXT NOT NULL
        CHECK (
            relationship_role IN (
                'Primary',
                'Associated',
                'Comparative'
            )
        ),

    PRIMARY KEY (case_id, location_id),

    FOREIGN KEY (case_id)
        REFERENCES research_case(case_id),

    FOREIGN KEY (location_id)
        REFERENCES location(location_id)
);


-- Reusable research organizations
CREATE TABLE IF NOT EXISTS organization (
    organization_id INTEGER PRIMARY KEY,
    organization_name TEXT NOT NULL UNIQUE,
    short_name TEXT,
    organization_type TEXT,
    website TEXT,
    general_location TEXT,
    description TEXT,
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- Individual research activities
CREATE TABLE IF NOT EXISTS research_activity (
    activity_id INTEGER PRIMARY KEY,
    activity_number TEXT NOT NULL UNIQUE,
    activity_name TEXT NOT NULL,

    activity_type TEXT NOT NULL
        CHECK (
            activity_type IN (
                'INV',
                'EXP',
                'HIS',
                'CMP',
                'COM'
            )
        ),

    activity_status TEXT NOT NULL DEFAULT 'Proposed'
        CHECK (
            activity_status IN (
                'Proposed',
                'Planning',
                'Ready',
                'In Progress',
                'On Hold',
                'Post-Research Review',
                'Completed',
                'Terminated'
            )
        ),

    purpose TEXT,
    planned_start_date TEXT,
    actual_start_date TEXT,
    actual_end_date TEXT,

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- Connect Research Activities to Cases
CREATE TABLE IF NOT EXISTS case_activity (
    case_id INTEGER NOT NULL,
    activity_id INTEGER NOT NULL,

    PRIMARY KEY (case_id, activity_id),

    FOREIGN KEY (case_id)
        REFERENCES research_case(case_id),

    FOREIGN KEY (activity_id)
        REFERENCES research_activity(activity_id)
);


-- Connect Organizations to Research Activities
CREATE TABLE IF NOT EXISTS activity_organization (
    activity_id INTEGER NOT NULL,
    organization_id INTEGER NOT NULL,

    organization_role TEXT NOT NULL
        CHECK (
            organization_role IN (
                'Lead',
                'Collaborating',
                'Contributing',
                'Supporting'
            )
        ),

    PRIMARY KEY (activity_id, organization_id),

    FOREIGN KEY (activity_id)
        REFERENCES research_activity(activity_id),

    FOREIGN KEY (organization_id)
        REFERENCES organization(organization_id)
);

-- Connect Research Activities to Locations
CREATE TABLE IF NOT EXISTS activity_location (
    activity_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,

    PRIMARY KEY (activity_id, location_id),

    FOREIGN KEY (activity_id)
        REFERENCES research_activity(activity_id),

    FOREIGN KEY (location_id)
        REFERENCES location(location_id)
);

-- Reusable people involved in research
CREATE TABLE IF NOT EXISTS person (
    person_id INTEGER PRIMARY KEY,
    display_name TEXT NOT NULL,
    given_name TEXT,
    family_name TEXT,
    notes TEXT,
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Connect people to Research Activities
CREATE TABLE IF NOT EXISTS activity_person (
    activity_id INTEGER NOT NULL,
    person_id INTEGER NOT NULL,

    participation_role TEXT NOT NULL
        CHECK (
            participation_role IN (
                'Activity Lead',
                'Investigator',
                'Researcher',
                'Evidence Reviewer',
                'Technical Support',
                'Observer'
            )
        ),

    PRIMARY KEY (activity_id, person_id),

    FOREIGN KEY (activity_id)
        REFERENCES research_activity(activity_id),

    FOREIGN KEY (person_id)
        REFERENCES person(person_id)
);

-- Time-bounded events within a Research Activity
CREATE TABLE IF NOT EXISTS research_event (
    event_id INTEGER PRIMARY KEY,
    activity_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    event_start TEXT NOT NULL,
    event_end TEXT,
    event_description TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (activity_id)
        REFERENCES research_activity(activity_id)
);

-- Observations recorded during Research Events
CREATE TABLE IF NOT EXISTS observation (
    observation_id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL,
    recorded_by_person_id INTEGER,
    observed_at TEXT NOT NULL,
    observation_type TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (event_id)
        REFERENCES research_event(event_id),

    FOREIGN KEY (recorded_by_person_id)
        REFERENCES person(person_id)
);

-- Materials collected or created during research
CREATE TABLE IF NOT EXISTS research_material (
    material_id INTEGER PRIMARY KEY,
    activity_id INTEGER NOT NULL,
    material_number TEXT NOT NULL UNIQUE,
    material_type TEXT NOT NULL
        CHECK (
            material_type IN (
                'Audio',
                'Video',
                'Photograph',
                'Document',
                'Instrument Data',
                'Other'
            )
        ),
    material_name TEXT NOT NULL,
    file_path TEXT,
    description TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (activity_id)
        REFERENCES research_activity(activity_id)
);

-- Connect Research Materials to the Events they document
CREATE TABLE IF NOT EXISTS event_material (
    event_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,

    PRIMARY KEY (event_id, material_id),

    FOREIGN KEY (event_id)
        REFERENCES research_event(event_id),

    FOREIGN KEY (material_id)
        REFERENCES research_material(material_id)
);


