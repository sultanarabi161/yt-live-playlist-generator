import requests
import json
import re
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0'
}

PLAYLIST_FILE = "playlist.m3u"
USERNAME_FILE = "username.json"

def get_live_video_id(channel_handle):
    try:
        url = f"https://www.youtube.com/{channel_handle}/live"
        r = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        final_url = r.url
        match = re.search(r'v=([a-zA-Z0-9_-]{11})', final_url)
        if match:
            return match.group(1)
    except Exception as e:
        print(f"Error fetching {channel_handle}: {e}")
    return None

def main():
    with open(USERNAME_FILE, "r", encoding="utf-8") as f:
        channels = json.load(f)

    m3u = "#EXTM3U\n"
    for ch in channels:
        video_id = get_live_video_id(ch["username"])
        print(f"{ch['name']} → video_id: {video_id}")
        if video_id:
            name = ch["name"]
            logo = ch["logo"]
            stream_url = f"https://m.xigzo.store/yt/live.php?video_id={video_id}"
            m3u += f"#EXTINF:-1 tvg-logo=\"{logo}\",{name}\n{stream_url}\n"

    m3u += f"\n# Auto-updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    m3u += "# Note: Use in media player like VLC. Not supported in browser.\n"

    with open(PLAYLIST_FILE, "w", encoding="utf-8") as f:
        f.write(m3u)

if __name__ == "__main__":
    main()
