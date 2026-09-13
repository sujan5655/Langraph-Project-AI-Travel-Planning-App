import os
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("AviationStack MCP")

API_URL = "https://api.aviationstack.com/v1"


def get_api_key():
    api_key = os.getenv("AVIATION_STACK_API_KEY")

    if not api_key:
        raise ValueError(
            "AVIATION_STACK_API_KEY is not set"
        )

    return api_key


@mcp.tool()
def list_airports(search: str = "", limit: int = 10):
    """Search airports using AviationStack."""

    params = {
        "access_key": get_api_key(),
        "limit": limit,
    }

    if search:
        params["search"] = search

    response = requests.get(
        f"{API_URL}/airports",
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise ValueError(str(data["error"]))

    return data.get("data", [])


@mcp.tool()
def list_airlines(search: str = "", limit: int = 10):
    """Search airlines using AviationStack."""

    params = {
        "access_key": get_api_key(),
        "limit": limit,
    }

    if search:
        params["search"] = search

    response = requests.get(
        f"{API_URL}/airlines",
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise ValueError(str(data["error"]))

    return data.get("data", [])


@mcp.tool()
def get_flights(
    dep_iata: str = "",
    arr_iata: str = "",
    limit: int = 10,
):
    """Get flights using AviationStack."""

    params = {
        "access_key": get_api_key(),
        "limit": limit,
    }

    if dep_iata:
        params["dep_iata"] = dep_iata

    if arr_iata:
        params["arr_iata"] = arr_iata

    response = requests.get(
        f"{API_URL}/flights",
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise ValueError(str(data["error"]))

    return data.get("data", [])


if __name__ == "__main__":
    mcp.run()
