from flask import Flask, request, jsonify, render_template from truecallerpy import search_phonenumber from datetime import datetime

app = Flask(name, template_folder="templates")

@app.route("/") def home(): return render_template("index.html")

@app.route("/api/simlookup", methods=["GET"]) def sim_lookup(): number = request.args.get("number")

if not number:
    return jsonify({"error": "Missing phone number"}), 400

try:
    # Use Truecaller API Wrapper
    response = search_phonenumber(number, "LK", "Mozilla/5.0")
    data = response.get("data", {})

    sim_data = {
        "number": number,
        "sim_type": data.get("phones", [{}])[0].get("type", "Unknown"),
        "operator": data.get("phones", [{}])[0].get("carrier", "Unknown"),
        "location": data.get("addresses", [{}])[0].get("city", "Sri Lanka"),
        "imei": "35-209900-176148-1",  # simulated
        "status": "Active",
        "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": data.get("name", "Unknown")
    }
    return jsonify(sim_data)

except Exception as e:
    return jsonify({"error": str(e)}), 500

if name == "main": app.run(host="0.0.0.0", port=5000)

