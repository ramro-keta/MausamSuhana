import os
import requests
from dotenv import load_dotenv


def get_weather(city_name: str, api_key: str) -> dict | None:
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "condition": data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
        }
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"Error: City '{city_name}' not found. Check spelling.")
        elif response.status_code == 401:
            print("Error: Invalid API Key. Check your OpenWeatherMap key.")
        else:
            print(f"HTTP Error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Network error occurred: {req_err}")

    return None


def map_weather_to_music(weather_condition: str) -> dict:
    mood_map = {
        "Clear": {
            "search_query": "upbeat summer hits",
            "description": "Bright and happy tunes for sunny weather",
        },
        "Rain": {
            "search_query": "cozy rainy day lo-fi chill",
            "description": "Cozy acoustic and lo-fi beats for rain",
        },
        "Drizzle": {
            "search_query": "indie folk rainy day",
            "description": "Melancholic indie and acoustic tracks",
        },
        "Clouds": {
            "search_query": "chill atmospheric post-rock",
            "description": "Atmospheric and relaxed tracks for overcast skies",
        },
        "Snow": {
            "search_query": "soft winter piano classical",
            "description": "Soft classical and piano pieces for snowy weather",
        },
        "Thunderstorm": {
            "search_query": "dramatic rock electronic storm",
            "description": "High-energy rock and dramatic soundscapes",
        },
    }
    default = {
        "search_query": "relaxing instrumental chill",
        "description": "Mellow ambient tracks",
    }
    return mood_map.get(weather_condition, default)


def get_music_recommendations(mood_info: dict, client_id: str) -> list[dict]:
    base_url = "https://api.jamendo.com/v3.0/tracks/"
    params = {
        "client_id": client_id,
        "format": "json",
        "limit": 5,
        "namesearch": mood_info["search_query"],
        "include": "musicinfo",
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        songs = []
        for item in data.get("results", []):
            songs.append(
                {
                    "title": item.get("name"),
                    "artist": item.get("artist_name"),
                    "url": item.get("shareurl"),
                    "audio_url": item.get("audio"),  # Full streaming audio link
                }
            )
        return songs
    except requests.exceptions.RequestException as err:
        print(f"Jamendo API Error: {err}")
        return []


if __name__ == "__main__":
    load_dotenv()

    # Load keys safely from environment variables or .env file
    OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")
    JAMENDO_CLIENT_ID = os.getenv("JAMENDO_CLIENT_ID")

    if not all([OPENWEATHER_KEY, JAMENDO_CLIENT_ID]):
        print(
            "Error: Missing API credentials. Ensure OPENWEATHER_KEY and JAMENDO_CLIENT_ID are in your .env file."
        )
        exit(1)

    city = input("Enter city: ").strip()
    if not city:
        print("Error: City name cannot be empty.")
        exit(1)

    weather = get_weather(city, OPENWEATHER_KEY)

    if weather:
        condition = weather["condition"]
        print(
            f"\nWeather in {weather['city']}: {condition} ({weather['temp']}°C)"
        )

        mood = map_weather_to_music(condition)
        print(f"Music Mood: {mood['description']}")

        songs = get_music_recommendations(mood, JAMENDO_CLIENT_ID)

        if songs:
            print("\n--- Recommended Songs ---")
            for idx, song in enumerate(songs, 1):
                print(f"{idx}. {song['title']} by {song['artist']}")
                print(f"   Listen: {song['url']}")
        else:
            print("No tracks found or failure connecting to Jamendo.")
