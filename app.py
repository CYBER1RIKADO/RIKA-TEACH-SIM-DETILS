from flask import Flask, request, jsonify
from datetime import datetime
import requests
import os

app = Flask(__name__)

# 🛡️ Set your Numverify API Key (replace YOUR_API_KEY or use env var)
NUMVERIFY_API_KEY = os.getenv("NUMVERIFY_API_KEY", "5d7960c0c4f869d51c80dd74fad572c6")

@app.route("/api/simlookup", methods=["GET"])
def sim_lookup():
    number = request.args.get("number")

    if not number:
        return jsonify({"error": "Missing phone number"}), 400

    # 🔎 Operator guess based on prefix
    operator_guess = "Unknown"
    if number.startswith(("70", "71")):
        operator_guess = "Mobitel"
    elif number.startswith(("72", "78")):
        operator_guess = "Hutch"
    elif number.startswith(("76", "77")):
        operator_guess = "Dialog"
    elif number.startswith(("75",)):
        operator_guess = "Airtel"

    # 🌐 Numverify API call
    api_url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={number}&country_code=LK&format=1"

    try:
        api_response = requests.get(api_url)
        api_data = api_response.json()

        if not api_data.get("valid"):
            return jsonify({"error": "Invalid phone number according to API"}), 400

        data = {
            "number": number,
            "sim_type": "4G LTE",
            "operator": operator_guess,
            "api_operator": api_data.get("carrier", "Unknown"),
            "location": api_data.get("location", "Sri Lanka"),
            "country": api_data.get("country_name", "Sri Lanka"),
            "country_code": api_data.get("country_code", "LK"),
            "line_type": api_data.get("line_type", "mobile"),
            "imei": "35-209900-176148-1",
            "status": "Active",
            "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": f"API Error: {str(e)}"}), 500


@app.route("/")
def home():
    return "SIM Lookup API by RIKA TECH with NumVerify"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
