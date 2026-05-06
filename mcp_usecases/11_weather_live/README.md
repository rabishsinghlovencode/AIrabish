# Weather MCP Tool 

An MCP (Model Context Protocol) server using the OpenWeatherMap API to provide:

- Real-time weather conditions
- 5-day weather forecasts


---

## 🚀 Setup

1. **Python 3.10+** is required.
2. Install dependencies:
   ```bash
   uv venv
   .venv\Scripts\activate
   uv add -r requirements.txt OR uv pip install -r requirements.txt
   ```
3. **Get an API key** from [OpenWeatherMap](https://openweathermap.org/api).
4. **Create a `.env` file** in the root folder:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```
5. Run the Server

   ```bash
   mcp dev main.py
   ```

---

## 🛠 Available Tools

### `get_current_weather(location: str)`
Returns current weather for a given location.

### `get_weather_forecast(location: str, days: int = 5)`
Returns a weather forecast (up to 5 days) for the location.

### `get_air_quality(location: str)`
Returns air quality metrics and AQI level.

### `search_location(query: str)`
Returns up to 5 location matches based on the query.

---

## 🧪 Example Output (India)

### Current Weather (Delhi)
```json
{
  "location": {
    "name": "Delhi",
    "country": "IN",
    "lat": 28.6139,
    "lon": 77.2090
  },
  "temperature": {
    "current": 32.4,
    "feels_like": 35.1,
    "min": 30.0,
    "max": 36.2
  },
  "weather_condition": {
    "main": "Haze",
    "description": "smoky haze",
    "icon": "50d"
  },
  "wind": {
    "speed": 4.1,
    "deg": 135
  },
  "clouds": 20,
  "humidity": 58,
  "pressure": 1005,
  "visibility": 5000,
  "sunrise": "2025-03-16T06:20:00",
  "sunset": "2025-03-16T18:40:00",
  "timestamp": "2025-03-16T14:30:00"
}
```

### Weather Forecast (Mumbai)
```json
{
  "location": {
    "name": "Mumbai",
    "country": "IN",
    "lat": 19.0760,
    "lon": 72.8777
  },
  "forecast": [
    {
      "datetime": "2025-03-16T12:00:00",
      "temperature": {
        "temp": 33.2,
        "feels_like": 37.8,
        "min": 31.5,
        "max": 34.0
      },
      "weather_condition": {
        "main": "Clouds",
        "description": "scattered clouds",
        "icon": "03d"
      },
      "wind": {
        "speed": 3.9,
        "deg": 200
      },
      "clouds": 40,
      "humidity": 70,
      "pressure": 1008,
      "visibility": 10000,
      "pop": 0.1
    }
  ],
  "days": 5
}
```

### Air Quality (Bangalore)
```json
{
  "location": {
    "name": "Bengaluru",
    "country": "IN",
    "lat": 12.9716,
    "lon": 77.5946
  },
  "air_quality_index": 2,
  "air_quality_level": "Fair",
  "components": {
    "co": 102.4,
    "no": 0.0,
    "no2": 12.6,
    "o3": 30.5,
    "so2": 3.8,
    "pm2_5": 45.1,
    "pm10": 60.2,
    "nh3": 1.5
  },
  "timestamp": "2025-03-16T14:30:00"
}
```

### Location Search
```json
{
  "results": [
    {
      "name": "Kolkata",
      "state": "West Bengal",
      "country": "IN",
      "lat": 22.5726,
      "lon": 88.3639
    },
    {
      "name": "Kolkata",
      "state": "",
      "country": "IN",
      "lat": 22.5675,
      "lon": 88.3700
    }
  ]
}
```

---

## 🧰 Error Handling

All tools return clear error messages:
```json
{ "error": "Location 'XYZ' not found" }
```

---

## 📌 Notes

- Ensure `.env` file is configured correctly.
- API keys may take time to activate.
- OpenWeatherMap free tier: 60 API calls per minute.

