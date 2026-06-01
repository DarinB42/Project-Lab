from pathlib import Path

from services.database_service import fetch_all_investigations

from flask import Flask

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
                <h3>{case_number}</h3>
                <p>Location: {location}</p>
                <p>Date: {investigation_date}</p>
                <p>Weather: {weather}</p>
                <p>Evidence Type: {evidence_type}</p>
                <hr>
            </div>
            """

    return html


if __name__ == "__main__":
    app.run(debug=True)