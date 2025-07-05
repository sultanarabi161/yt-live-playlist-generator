import requests
import json
import re
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36'
}

PLAYLIST_FILE = "playlist.m3u"
USERNAME_FILE = "username.json"


def get_live_video_id(channel_handle):
    url = f"https://www.youtube.com/{channel_handle}/live"
    try:
        html = requests.get(url, headers=HEADERS, timeout=10).text
        match = re.search(r'<meta property="og:url" content="https://www.youtube.com/watch\?v=([^"]+)', html)
        if match:
            return match.group(1)
    except Exception as e:
        print(f"Error fetching {channel_handle}: {e}")
        return None
    return None


def main():
    with open(USERNAME_FILE, "r", encoding="utf-8") as f:
        channels = json.load(f)

    m3u = "#EXTM3U\n"
    for ch in channels:
        video_id = get_live_video_id(ch["username"])
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
