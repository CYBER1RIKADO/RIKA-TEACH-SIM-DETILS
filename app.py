from flask import Flask, request, jsonify, render_template
from truecallerpy import search_phonenumber
from datetime import datetime

app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/simlookup", methods=["GET"])
def sim_lookup():
    number = request.args.get("number")

    if not number:
        return jsonify({"error": "Missing phone number"}), 400

    try:
        response = search_phonenumber(number, "LK", "Mozilla/5.0")
        data = response.get("data", {})

        phones = data.get("phones", [{}])
        addresses = data.get("addresses", [{}])

        sim_data = {
            "number": number,
            "name": data.get("name", "Unknown"),
            "sim_type": phones[0].get("type", "Unknown"),
            "operator": phones[0].get("carrier", "Unknown"),
            "location": addresses[0].get("city", "Sri Lanka"),
            "imei": "35-209900-176148-1",
            "status": "Active",
            "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        return jsonify(sim_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
