from __future__ import annotations

from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather Advice")





WEATHER = {"hyderabad": "hot", "delhi": "rainy", "mumbai": "humid"}

@mcp.tool()
def get_weather(city: str) -> str:
    """Return sample weather state for a city."""
    return WEATHER.get(city.lower(), "pleasant")

@mcp.tool()
def suggest_action(weather: str) -> str:
    """Suggest what to do based on weather."""
    weather = weather.lower()
    if weather == "hot":
        return "Carry water and wear light clothes."
    if weather == "rainy":
        return "Carry an umbrella."
    if weather == "humid":
        return "Stay hydrated."
    return "Enjoy your day."



if __name__ == "__main__":
    mcp.run()
