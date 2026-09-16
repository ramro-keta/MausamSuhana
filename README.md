# MausamSuhana
## 🎵 Weather Mood Player

A Python application that fetches real-time weather data for any given city and automatically recommends matching Spotify music based on the weather mood.

---

## 🌟 Features
- Real-time weather lookup using OpenWeatherMap API.
- Intelligent weather-to-music mapping (e.g., Rain -> Cozy Lo-Fi / Acoustic, Clear -> Upbeat Summer Pop).
- Automated track recommendations via Spotify API.

---

## 🛠️ Tech Stack & Libraries
- **Language:** Python 3
- **Libraries:** `requests`, `spotipy`, `python-dotenv`
- **APIs:** OpenWeatherMap API, Spotify Web API

---

## 🚀 Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/weather-music-app.git](https://github.com/your-username/weather-music-app.git)
   cd weather-music-app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and add your OpenWeatherMap and Spotify API credentials.

4. **Run the App:**
   ```bash
   python main.py
   ```
