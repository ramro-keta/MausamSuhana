import os
import requests
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials


def get_weather(city_name, api_key):
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
            print(f"Error: City '{city_name}' not found. Please check spelling.")
        elif response.status_code == 401:
            print("Error: Invalid API Key. Check your OpenWeatherMap key.")
        else:
            print(f"HTTP Error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Network error occurred: {req_err}")

    return None


def map_weather_to_music(weather_condition):
    mood_map = {
        "Clear": {
            "genre": "pop",
            "search_query": "upbeat summer hits",
            "target_valence": 0.8,
            "description": "Bright and happy tunes for sunny weather",
        },
        "Rain": {
            "genre": "acoustic",
            "search_query": "cozy rainy day lo-fi chill",
            "target_valence": 0.3,
            "description": "Cozy acoustic and lo-fi beats for rain",
        },
        "Drizzle": {
            "genre": "indie",
            "search_query": "indie folk rainy day",
            "target_valence": 0.4,
            "description": "Melancholic indie and acoustic tracks",
        },
        "Clouds": {
            "genre": "ambient",
            "search_query": "chill atmospheric post-rock",
            "target_valence": 0.5,
            "description": "Atmospheric and relaxed tracks for overcast skies",
        },
        "Snow": {
            "genre": "classical",
            "search_query": "soft winter piano classical",
            "target_valence": 0.4,
            "description": "Soft classical and piano pieces for snowy weather",
        },
        "Thunderstorm": {
            "genre": "rock",
            "search_query": "dramatic rock electronic storm",
            "target_valence": 0.5,
            "description": "High-energy rock and dramatic soundscapes",
        },
    }
    default = {
        "genre": "chill",
        "search_query": "relaxing instrumental chill",
        "target_valence": 0.5,
        "description": "Mellow ambient tracks",
    }
    return mood_map.get(weather_condition, default)


def get_music_recommendations(mood_info, client_id, client_secret):
    auth_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    results = sp.search(q=mood_info["search_query"], type="track", limit=5)

    songs = []
    for item in results["tracks"]["items"]:
        songs.append(
            {
                "title": item["name"],
                "artist": item["artists"][0]["name"],
                "url": item["external_urls"]["spotify"],
                "preview_url": item["preview_url"],
            }
        )
    return songs


if __name__ == "__main__":
    load_dotenv()

    # Load keys safely from environment variables or .env file
    OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY", "YOUR_OPENWEATHER_KEY")
    SPOTIFY_CLIENT_ID = os.getenv(
        "SPOTIFY_CLIENT_ID", "YOUR_SPOTIFY_CLIENT_ID"
    )
    SPOTIFY_CLIENT_SECRET = os.getenv(
        "SPOTIFY_CLIENT_SECRET", "YOUR_SPOTIFY_CLIENT_SECRET"
    )

    city = input("Enter city: ")
    weather = get_weather(city, OPENWEATHER_KEY)

    if weather:
        condition = weather["condition"]
        print(
            f"\nWeather in {weather['city']}: {condition} ({weather['temp']}°C)"
        )

        mood = map_weather_to_music(condition)
        print(f"Music Mood: {mood['description']}")

        songs = get_music_recommendations(
            mood, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
        )

        print("\n--- Recommended Songs ---")
        for idx, song in enumerate(songs, 1):
            print(f"{idx}. {song['title']} by {song['artist']}")
            print(f"   Listen: {song['url']}")
