from fastmcp import FastMCP

mcp = FastMCP("Weather Server")


@mcp.tool()
def get_weather(city: str):
    """回傳指定城市的天氣資訊。"""

    # 模擬天氣資料
    weather_data = {
        "Delhi": "Sunny, 32°C",
        "Paris": "Cloudy, 9°C",
        "Sydney": "Rainy, 29°C",
        "London": "Partly cloudy, 15°C"}

    # 回傳天氣資料，如果城市不存在則回傳 "Weather data not available."
    return weather_data.get(city, "Weather data not available.")


if __name__ == "__main__":
    print("Starting Weather MCP Server...")
    mcp.run()
