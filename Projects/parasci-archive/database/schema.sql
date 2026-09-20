
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

