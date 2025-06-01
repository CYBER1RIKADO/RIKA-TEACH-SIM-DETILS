from flask import Flask, request, jsonify, render_template
from datetime import datetime
import os
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/simlookup", methods=["GET"])
def sim_lookup():
    number = request.args.get("number")

    if not number:
        return jsonify({"error": "Missing phone number"}), 400

    # Local detection (SL-based operator)
    operator = "Unknown"
    if number.startswith(("70", "71")):
        operator = "Mobitel"
    elif number.startswith(("72", "78")):
        operator = "Hutch"
    elif number.startswith(("76", "77")):
        operator = "Dialog"
    elif number.startswith("75"):
        operator = "Airtel"

    # External NumVerify API
    api_key = os.getenv("NUMVERIFY_API_KEY")
    api_url = f"http://apilayer.net/api/validate?access_key={api_key}&number={number}&country_code=LK"

    try:
        response = requests.get(api_url)
        api_data = response.json()
    except Exception as e:
        return jsonify({"error": "Failed to contact external API"}), 500

    # Merge data
    data = {
        "number": number,
        "sim_type": "4G LTE",
        "operator": operator,
        "location": api_data.get("location", "Sri Lanka"),
        "imei": "35-209900-176148-1",
        "status": "Active",
        "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
