from flask import Flask, render_template, redirect, url_for

from database import initialize_database, get_alerts
from detector import analyze_events


app = Flask(__name__)

initialize_database()


@app.route("/")
def index():
    alerts = get_alerts()

    return render_template(
        "index.html",
        alerts=alerts
    )


@app.route("/analyze")
def analyze():
    filename = "logs/network.log"

    try:
        analyze_events(filename)
    except FileNotFoundError:
        return "Network log file was not found.", 404

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
