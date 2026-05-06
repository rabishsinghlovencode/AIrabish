from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
import logging
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("weather-mcp")

# API Key from environment variables
API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    logger.warning("OpenWeather API key not found in environment variables. Please set OPENWEATHER_API_KEY in your .env file.")

BASE_URL = "https://api.openweathermap.org/data/2.5"
GEO_URL = "https://api.openweathermap.org/geo/1.0"

@mcp.tool("get_current_weather")
async def get_current_weather(location: str) -> Dict[str, Any]:
    """Get current weather conditions for a location.
    
    Args:
        location (str): City name, state code (optional), country code (optional)
                       e.g., "London", "New York,US", "Paris,FR"
    
    Returns:
        Dict containing current weather data
    """
    try:
        if not API_KEY:
            return {"error": "OpenWeather API key not configured. Please set OPENWEATHER_API_KEY in your .env file."}
            
        # Get coordinates using geocoding API
        geo_response = requests.get(f"{GEO_URL}/direct?q={location}&limit=1&appid={API_KEY}")
        geo_data = geo_response.json()
        
        # Check for API errors
        if isinstance(geo_data, dict) and geo_data.get('cod') in [401, '401']:
            return {"error": f"API Key error: {geo_data.get('message', 'Invalid API key')}"}
        
        if not geo_data or len(geo_data) == 0:
            return {"error": f"Location '{location}' not found"}
        
        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]
        place_name = geo_data[0]["name"]
        country = geo_data[0].get("country", "")
        
        # Get current weather data
        weather_response = requests.get(
            f"{BASE_URL}/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        )
        weather_data = weather_response.json()
        
        if weather_response.status_code != 200:
            return {"error": f"Weather data not available: {weather_data.get('message', 'Unknown error')}"}
            
        weather = {
            "location": {
                "name": place_name,
                "country": country,
                "lat": lat,
                "lon": lon
            },
            "temperature": {
                "current": weather_data["main"]["temp"],
                "feels_like": weather_data["main"]["feels_like"],
                "min": weather_data["main"]["temp_min"],
                "max": weather_data["main"]["temp_max"]
            },
            "weather_condition": {
                "main": weather_data["weather"][0]["main"],
                "description": weather_data["weather"][0]["description"],
                "icon": weather_data["weather"][0]["icon"]
            },
            "wind": {
                "speed": weather_data["wind"]["speed"],
                "deg": weather_data["wind"]["deg"]
            },
            "clouds": weather_data["clouds"]["all"],
            "humidity": weather_data["main"]["humidity"],
            "pressure": weather_data["main"]["pressure"],
            "visibility": weather_data.get("visibility", 0),
            "sunrise": datetime.fromtimestamp(weather_data["sys"]["sunrise"]).isoformat(),
            "sunset": datetime.fromtimestamp(weather_data["sys"]["sunset"]).isoformat(),
            "timestamp": datetime.fromtimestamp(weather_data["dt"]).isoformat()
        }
        
        return weather
    except Exception as e:
        logger.error(f"Error fetching current weather for {location}: {str(e)}")
        return {"error": f"Failed to fetch current weather for {location}: {str(e)}"}

@mcp.tool("get_weather_forecast")
async def get_weather_forecast(location: str, days: int = 5) -> Dict[str, Any]:
    """Get weather forecast for a location.
    
    Args:
        location (str): City name, state code (optional), country code (optional)
                       e.g., "London", "New York,US", "Paris,FR"
        days (int): Number of days for forecast (1-5)
    
    Returns:
        Dict containing forecast data
    """
    try:
        if not API_KEY:
            return {"error": "OpenWeather API key not configured. Please set OPENWEATHER_API_KEY in your .env file."}
            
        # Limit days to valid range
        days = max(1, min(5, days))
        
        # Get coordinates using geocoding API
        geo_response = requests.get(f"{GEO_URL}/direct?q={location}&limit=1&appid={API_KEY}")
        geo_data = geo_response.json()
        
        # Check for API errors
        if isinstance(geo_data, dict) and geo_data.get('cod') in [401, '401']:
            return {"error": f"API Key error: {geo_data.get('message', 'Invalid API key')}"}
        
        if not geo_data or len(geo_data) == 0:
            return {"error": f"Location '{location}' not found"}
        
        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]
        place_name = geo_data[0]["name"]
        country = geo_data[0].get("country", "")
        
        # Get forecast data
        forecast_response = requests.get(
            f"{BASE_URL}/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&cnt={days*8}"
        )
        forecast_data = forecast_response.json()
        
        if forecast_response.status_code != 200:
            return {"error": f"Forecast data not available: {forecast_data.get('message', 'Unknown error')}"}
            
        forecast_list = forecast_data["list"]
        
        # Process forecast data
        forecast_items = []
        for item in forecast_list:
            forecast_items.append({
                "datetime": datetime.fromtimestamp(item["dt"]).isoformat(),
                "temperature": {
                    "temp": item["main"]["temp"],
                    "feels_like": item["main"]["feels_like"],
                    "min": item["main"]["temp_min"],
                    "max": item["main"]["temp_max"]
                },
                "weather_condition": {
                    "main": item["weather"][0]["main"],
                    "description": item["weather"][0]["description"],
                    "icon": item["weather"][0]["icon"]
                },
                "wind": {
                    "speed": item["wind"]["speed"],
                    "deg": item["wind"]["deg"]
                },
                "clouds": item["clouds"]["all"],
                "humidity": item["main"]["humidity"],
                "pressure": item["main"]["pressure"],
                "visibility": item.get("visibility", 0),
                "pop": item.get("pop", 0)  # Probability of precipitation
            })
        
        return {
            "location": {
                "name": place_name,
                "country": country,
                "lat": lat,
                "lon": lon
            },
            "forecast": forecast_items,
            "days": days
        }
    except Exception as e:
        logger.error(f"Error fetching forecast for {location}: {str(e)}")
        return {"error": f"Failed to fetch forecast for {location}: {str(e)}"}

if __name__ == "__main__":
    # Print API key status (without revealing the key)
    if API_KEY:
        logger.info("OpenWeather API key loaded successfully")
    else:
        logger.warning("OpenWeather API key not found. Please set OPENWEATHER_API_KEY in your .env file.")
    
    # Run the MCP server
    mcp.run(transport="sse")