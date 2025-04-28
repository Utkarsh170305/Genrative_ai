from flask import Flask, render_template, request, jsonify
import subprocess
import requests
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    """Serve the main page."""
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    """
    Handle the prompt from the frontend and call Ollama CLI for generation.
    Now includes an optional 'city' for weather.
    """
    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    city = data.get("city", "").strip()  # City input from front-end

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Date/Time Handling
    if "date" in prompt.lower() or "time" in prompt.lower():
        now = datetime.now()
        return jsonify({"completion": f"The current date and time is {now.strftime('%Y-%m-%d %H:%M:%S')}."})

    # Weather API Handling
    if "weather" in prompt.lower():
        if not city:
            city = "London"  # Default to London if no city is provided
        api_key = "your_openweathermap_api_key"  # Replace with your actual API key
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(weather_url, timeout=5)  # Timeout for faster response
            weather_data = response.json()
            if response.status_code == 200:
                description = weather_data["weather"][0]["description"]
                temp = weather_data["main"]["temp"]
                return jsonify({"completion": f"The weather in {city} is {description} with a temperature of {temp}°C."})
            else:
                return jsonify({"completion": f"Unable to fetch weather data for {city}."})
        except Exception as e:
            return jsonify({"completion": f"Error fetching weather: {str(e)}"})

    # Default: Call the Ollama CLI
    try:
        result = subprocess.run(
            ["ollama", "run", "deepseek-r1:8b", prompt],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        if result.returncode == 0:
            return jsonify({"completion": result.stdout.strip()})
        else:
            return jsonify({"error": result.stderr.strip() or "Unknown error occurred."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
