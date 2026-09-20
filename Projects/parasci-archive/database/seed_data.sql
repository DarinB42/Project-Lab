
-- ParaSci Archive Prototype #2
-- Initial reference data

-- Research domains
INSERT OR IGNORE INTO domain
    (domain_id, domain_name, description)
VALUES
    (1, 'Hauntings & Apparitions',
        'Research involving reported hauntings, apparitions, and related phenomena.'),

    (2, 'Consciousness & Psi',
        'Research involving consciousness and reported psi phenomena.'),

    (3, 'UAP & Aerial Anomalies',
        'Research involving unidentified aerial phenomena.'),

    (4, 'Cryptids & Unidentified Biological Phenomena',
        'Research involving reported unidentified biological phenomena.'),

    (5, 'Occult & Esoteric Traditions',
        'Research involving occult and esoteric traditions.'),

    (6, 'Folklore & Historical Anomalies',
        'Research involving folklore and historical anomalous reports.'),

    (7, 'Cross-Phenomena Research',
        'Research involving questions that span multiple research domains.');

-- Initial Case statuses
INSERT OR IGNORE INTO case_status
    (case_status_id, status_name, description)
VALUES
    (1, 'Active',
        'The Case is open and research is being pursued.'),

    (2, 'Monitoring',
        'The Case remains open for new information or future research.'),

    (3, 'On Hold',
        'Research is temporarily paused.'),

    (4, 'Closed',
        'No further research is currently planned.');
