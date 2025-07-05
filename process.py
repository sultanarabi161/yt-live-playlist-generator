import requests
import json
from datetime import datetime

USERNAME_FILE = "username.json"
PLAYLIST_FILE = "playlist.m3u"
API_KEY_URL = "https://m.xigzo.store/apikey.json"

def get_api_key():
    try:
        return requests.get(API_KEY_URL).json()["api_key"]
    except:
        return None

def get_channel_id(username, api_key):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=id&forUsername={username.lstrip('@')}&key={api_key}"
    r = requests.get(url).json()
    if "items" in r and len(r["items"]) > 0:
        return r["items"][0]["id"]
    else:
        search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&q={username}&key={api_key}"
        r2 = requests.get(search_url).json()
        if "items" in r2 and len(r2["items"]) > 0:
            return r2["items"][0]["snippet"]["channelId"]
    return None

def get_live_video_id(channel_id, api_key):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&eventType=live&type=video&key={api_key}"
    r = requests.get(url).json()
    if "items" in r and len(r["items"]) > 0:
        return r["items"][0]["id"]["videoId"]
    return None

def main():
    with open(USERNAME_FILE, "r", encoding="utf-8") as f:
        channels = json.load(f)

    api_key = get_api_key()
    if not api_key:
        print(" API key not found!")
        return

    m3u = "#EXTM3U\n"
    for ch in channels:
        name = ch["name"]
        username = ch["username"]
        logo = ch["logo"]

        print(f" Checking {name} ({username})...")
        channel_id = get_channel_id(username, api_key)
        if not channel_id:
            print(f" Channel ID not found for {username}")
            continue

        video_id = get_live_video_id(channel_id, api_key)
        if video_id:
            stream_url = f"https://m.xigzo.store/yt/live.php?video_id={video_id}"
            m3u += f"#EXTINF:-1 tvg-logo=\"{logo}\",{name}\n{stream_url}\n"
            print(f" LIVE: {name}")
        else:
            print(f" OFFLINE: {name}")

    m3u += f"\n# Auto-updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    m3u += "# Note: Use in media player like VLC. Not supported in browser.\n"

    with open(PLAYLIST_FILE, "w", encoding="utf-8") as f:
        f.write(m3u)

if __name__ == "__main__":
    main()
