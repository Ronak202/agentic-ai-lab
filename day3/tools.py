import datetime

def calculator(expression):
    """Evaluate a math expression."""
    try:
        result = eval(expression)
        return f"Calculation result: {result}"
    except Exception as e:
        return f"Error: {e}"

def get_weather(city="Mumbai"):
    """Mock weather tool (replace with real API if desired)."""
    mock_data = {
        "mumbai": {"temp": "32°C", "condition": "Humid and cloudy"},
        "delhi":  {"temp": "28°C", "condition": "Sunny"},
        "london": {"temp": "15°C", "condition": "Rainy"},
    }
    data = mock_data.get(city.lower(), {"temp": "N/A", "condition": "City not found"})
    return f"Weather in {city}: {data['temp']}, {data['condition']}"

def summarize_text(text):
    """Simple extractive summarizer."""
    sentences = text.split('.')
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
    summary = '. '.join(sentences[:2])
    return f"Summary: {summary}." if summary else "Text too short to summarize."

TOOLS = {
    "calculator": calculator,
    "weather":    get_weather,
    "summarize":  summarize_text,
}
