from pathlib import Path

from services.database_service import fetch_all_investigations

from flask import Flask

from services.database_service import (
    fetch_all_investigations,
    fetch_investigation_by_case
)

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>Investigation Log Generator</h1>
    <p>Web interface is running.</p>

    <ul>
        <li><a href="/investigations">View Investigations</a></li>
    </ul>
    """

@app.route("/investigations")
def investigations():

    database_folder = BASE_DIR / "database"

    investigations = fetch_all_investigations(database_folder)

    html = """
    <h1>Investigations</h1>
    <a href="/">Home</a>
    <hr>
    """

    if not investigations:
        html += "<p>No investigations found.</p>"

    else:
        for case_number, location, investigation_date, weather, evidence_type in investigations:

            html += f"""
            <div>
                <h3>
                    <a href="/investigation/{case_number}">
                        {case_number}
                    </a>
                </h3>
                <p>Location: {location}</p>
                <p>Date: {investigation_date}</p>
                <p>Weather: {weather}</p>
                <p>Evidence Type: {evidence_type}</p>
                <hr>
            </div>
            """

    return html

@app.route("/investigation/<case_number>")
def investigation_detail(case_number):

    database_folder = BASE_DIR / "database"

    result = fetch_investigation_by_case(
        database_folder,
        case_number
    )

    if result is None:
        return "<h1>Investigation not found</h1>"

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

    return f"""
    <h1>{case_number}</h1>

    <a href="/investigations">
        Back to Investigations
    </a>

    <hr>

    <p><strong>Location:</strong> {location}</p>
    <p><strong>Date:</strong> {investigation_date}</p>
    <p><strong>Investigators:</strong> {investigators}</p>
    <p><strong>Weather:</strong> {weather}</p>
    <p><strong>Evidence Type:</strong> {evidence_type}</p>
    <p><strong>Reported Activity:</strong> {reported_activity}</p>
    <p><strong>Equipment Used:</strong> {equipment_used}</p>
    <p><strong>Observations:</strong> {observations}</p>
    <p><strong>Initial Conclusion:</strong> {initial_conclusion}</p>
    <p><strong>Generated On:</strong> {generated_on}</p>
    """

if __name__ == "__main__":
    app.run(debug=True)