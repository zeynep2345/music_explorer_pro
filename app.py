from flask import Flask, render_template, request, redirect, url_for
import requests
import json
import os

app = Flask(__name__)

DEEZER_API_URL = "https://api.deezer.com/search"
DATA_FILE = "saved_songs.json"


def load_songs():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_songs(songs):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(songs, f, ensure_ascii=False, indent=2)


@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    songs = []
    saved_songs = load_songs()

    if request.method == "POST":
        query = request.form.get("query")
        response = requests.get(f"{DEEZER_API_URL}?q={query}")

        if response.status_code == 200:
            data = response.json()
            for item in data["data"][:10]:
                songs.append({
                    "title": item["title"],
                    "artist": item["artist"]["name"],
                    "album": item["album"]["title"],
                    "image": item["album"]["cover_medium"],
                    "preview": item["preview"]
                })

    return render_template(
        "index.html",
        songs=songs,
        saved_songs=saved_songs,
        query=query
    )


@app.route("/save", methods=["POST"])
def save():
    song = {
        "title": request.form["title"],
        "artist": request.form["artist"],
        "album": request.form["album"],
        "image": request.form["image"],
        "preview": request.form["preview"]
    }

    songs = load_songs()

    # Aynı şarkıyı iki kere kaydetmemek için
    if song not in songs:
        songs.append(song)
        save_songs(songs)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
