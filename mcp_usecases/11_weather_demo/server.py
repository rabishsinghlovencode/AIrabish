from __future__ import annotations

from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather Demo")





WEATHER = {"hyderabad": "33C and partly cloudy", "delhi": "28C and rainy", "mumbai": "31C and humid"}

@mcp.tool()
def get_weather(city: str) -> str:
    """Return sample weather data for a city."""
    return WEATHER.get(city.lower(), "weather not available")



if __name__ == "__main__":
    mcp.run()
