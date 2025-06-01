from flask import Flask, request, jsonify, render_template
from truecallerpy import search_phonenumber
from datetime import datetime
import asyncio

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
        # Run the async Truecaller API function in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(search_phonenumber(number, "LK", "Mozilla/5.0"))

        data = response.get("data", {})

        sim_data = {
            "number": number,
            "sim_type": data.get("phones", [{}])[0].get("type", "Unknown"),
            "operator": data.get("phones", [{}])[0].get("carrier", "Unknown"),
            "location": data.get("addresses", [{}])[0].get("city", "Sri Lanka"),
            "imei": "35-209900-176148-1",  # Simulated IMEI
            "status": "Active",
            "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": data.get("name", "Unknown")
        }
        return jsonify(sim_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
