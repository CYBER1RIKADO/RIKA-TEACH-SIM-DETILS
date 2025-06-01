// server.js
const express = require("express");
const axios = require("axios");
const app = express();

app.use(express.json());
app.use(express.static("public"));

const API_KEY = "5d7960c0c4f869d51c80dd74fad572c6";

app.get("/api/simlookup", async (req, res) => {
  const number = req.query.number;
  if (!number) return res.status(400).json({ error: "No number provided" });

  try {
    const response = await axios.get(
      `http://apilayer.net/api/validate?access_key=${API_KEY}&number=${number}`
    );
    const data = response.data;
    if (!data.valid) return res.status(404).json({ error: "Invalid number" });
    res.json({
      number: data.international_format,
      country: data.country_name,
      carrier: data.carrier,
      location: data.location,
      line_type: data.line_type,
    });
  } catch (err) {
    res.status(500).json({ error: "API request failed" });
  }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
