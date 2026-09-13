# pip install mcp requests python-dotenv

from mcp.server.fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Weather Server")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


@mcp.tool()
def get_current_weather(city: str):
    """Get current weather for a city."""
    if not OPENWEATHER_API_KEY:
        return {"error": "OPENWEATHER_API_KEY is not set"}

    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
        },
        timeout=15,
    )

    data = response.json()

    if response.status_code != 200:
        return {
            "error": data.get("message", "Failed to fetch weather"),
            "status_code": response.status_code,
        }

    return {
        "city": data["name"],
        "temperature_c": data["main"]["temp"],
        "feels_like_c": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
    }


@mcp.tool()
def get_forecast(city: str):
    """Get short weather forecast for a city."""
    if not OPENWEATHER_API_KEY:
        return {"error": "OPENWEATHER_API_KEY is not set"}

    response = requests.get(
        "https://api.openweathermap.org/data/2.5/forecast",
        params={
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
        },
        timeout=15,
    )

    data = response.json()

    # ---- THIS IS THE IMPORTANT FIX ----
    if response.status_code != 200 or "list" not in data:
        return {
            "error": data.get("message", "Failed to fetch forecast"),
            "status_code": response.status_code,
            "raw": data,
        }

    forecast = []
    for item in data["list"][:8]:  # first ~24 hours
        forecast.append(
            {
                "datetime": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "weather": item["weather"][0]["description"],
            }
        )

    return {
        "city": city,
        "forecast": forecast,
    }


if __name__ == "__main__":
    mcp.run()