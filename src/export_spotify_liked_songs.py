import os
import csv
import time
from typing import List, Dict, Any

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException



# Observacao: comentarios sem acentos.


load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "").strip()
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "").strip()  # deixe vazio para PKCE
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8080/callback").strip()
OUTPUT_CSV = os.getenv("OUTPUT_CSV", "spotify_liked_songs.csv").strip()

SCOPE = "user-library-read"

if not CLIENT_ID:
    raise SystemExit("SPOTIFY_CLIENT_ID ausente. Defina no .env")

# Dica: se CLIENT_SECRET estiver vazio, o Spotipy usa PKCE automaticamente
auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=(CLIENT_SECRET if CLIENT_SECRET else None),
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    open_browser=True,
    cache_path=".cache-liked-songs",
    show_dialog=False,
)

sp = spotipy.Spotify(auth_manager=auth_manager)

def safe_call(func, *args, **kwargs):
    max_retries = 5
    for attempt in range(1, max_retries + 1):
        try:
            return func(*args, **kwargs)
        except SpotifyException as e:
            if e.http_status == 429:
                retry_after = int(e.headers.get("Retry-After", "1"))
                time.sleep(retry_after + 1)
            else:
                raise
        except Exception:
            if attempt == max_retries:
                raise
            time.sleep(1 + attempt)

def extract_row(item: Dict[str, Any]) -> Dict[str, Any]:
    added_at = item.get("added_at", "")
    track = item.get("track") or {}
    if not track:
        return {
            "added_at": added_at, "track_name": "", "artists": "", "album": "",
            "album_release_date": "", "duration_ms": "", "popularity": "",
            "explicit": "", "track_url": "", "isrc": ""
        }

    artists = ", ".join([a.get("name", "") for a in (track.get("artists") or [])])
    album_obj = track.get("album") or {}
    external_urls = track.get("external_urls") or {}
    external_ids = track.get("external_ids") or {}

    return {
        "added_at": added_at,
        "track_name": track.get("name", ""),
        "artists": artists,
        "album": album_obj.get("name", ""),
        "album_release_date": album_obj.get("release_date", ""),
        "duration_ms": track.get("duration_ms", ""),
        "popularity": track.get("popularity", ""),
        "explicit": track.get("explicit", ""),
        "track_url": external_urls.get("spotify", ""),
        "isrc": external_ids.get("isrc", ""),
    }

def fetch_all_liked_tracks() -> List[Dict[str, Any]]:
    results = []
    limit = 50
    offset = 0
    while True:
        page = safe_call(sp.current_user_saved_tracks, limit=limit, offset=offset)
        items = page.get("items", [])
        for it in items:
            results.append(extract_row(it))
        if not page.get("next"):
            break
        offset += limit
    return results

def write_csv(rows: List[Dict[str, Any]], path: str) -> None:
    fieldnames = [
        "added_at","track_name","artists","album","album_release_date",
        "duration_ms","popularity","explicit","track_url","isrc",
    ]
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

def main():
    print("Baixando musicas curtidas...")
    rows = fetch_all_liked_tracks()
    write_csv(rows, OUTPUT_CSV)
    print(f"Concluido. {len(rows)} faixas exportadas para: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
