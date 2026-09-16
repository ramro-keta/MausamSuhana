import os
import requests
from dotenv import load_dotenv


def map_weather_to_music(weather_condition: str) -> dict:
    # Jamendo uses "tags" for genre/mood filtering
    mood_map = {
        "Clear": {"tag": "pop", "description": "Bright and happy pop tunes"},
        "Rain": {"tag": "lofi", "description": "Cozy lo-fi beats for rain"},
        "Drizzle": {"tag": "indie", "description": "Melancholic indie tracks"},
        "Clouds": {"tag": "ambient", "description": "Atmospheric chill tracks"},
        "Snow": {"tag": "classical", "description": "Soft classical and piano pieces"},
        "Thunderstorm": {"tag": "rock", "description": "Dramatic high-energy rock"},
    }
    return mood_map.get(
        weather_condition, {"tag": "chill", "description": "Mellow ambient tracks"}
    )


def get_music_recommendations(mood_info: dict, client_id: str) -> list[dict]:
    url = "https://api.jamendo.com/v3.0/tracks/"
    params = {
        "client_id": client_id,
        "format": "json",
        "limit": 5,
        "tags": mood_info["tag"],
        "boost": "popularity_month",  # Fetch popular tracks
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        songs = []
        for item in data.get("results", []):
            songs.append(
                {
                    "title": item["name"],
                    "artist": item["artist_name"],
                    "url": item["shareurl"],
                    "audio_stream": item["audio"],  # Direct playable MP3 link!
                }
            )
        return songs
    except requests.exceptions.RequestException as e:
        print(f"Jamendo API Error: {e}")
        return []


if __name__ == "__main__":
    load_dotenv()
    JAMENDO_CLIENT_ID = os.getenv("JAMENDO_CLIENT_ID")

    # Example query execution
    mood = map_weather_to_music("Rain")
    if JAMENDO_CLIENT_ID:
        songs = get_music_recommendations(mood, JAMENDO_CLIENT_ID)
        for idx, song in enumerate(songs, 1):
            print(f"{idx}. {song['title']} by {song['artist']}")
            print(f"   Audio MP3: {song['audio_stream']}")
