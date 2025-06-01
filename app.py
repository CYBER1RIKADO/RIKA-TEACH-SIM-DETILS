@app.route("/api/simlookup", methods=["GET"])
def sim_lookup():
    number = request.args.get("number")
    if not number:
        return jsonify({"error": "Missing number parameter"}), 400

    fake_data = {
        "number": number,
        "sim_type": "4G LTE",
        "operator": random.choice(["Dialog", "Mobitel", "Hutch"]),
        "location": f"{random.choice(['Colombo', 'Kandy', 'Galle'])}, Sri Lanka",
        "imei": f"35-{random.randint(100000,999999)}-{random.randint(100000,999999)}-1",
        "status": "Active",
        "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return jsonify(fake_data)
