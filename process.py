import requests
import json
from datetime import datetime

# Direct API key (for practice only)
API_KEY = "AIzaSyDiCm4f3jeHF-pp6mlGttanJXC53D_Pvcs"
PLAYLIST_FILE = "playlist.m3u"
USERNAME_FILE = "username.json"

def fetch_youtube_data(url):
    try:
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"API Error: {e}")
        return None

def get_channel_id(username):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={username}&type=channel&key={API_KEY}"
    data = fetch_youtube_data(url)
    return data['items'][0]['id']['channelId'] if data and 'items' in data else None

def get_live_video_id(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&eventType=live&type=video&key={API_KEY}"
    data = fetch_youtube_data(url)
    return data['items'][0]['id']['videoId'] if data and 'items' in data else None

def generate_playlist():
    with open(USERNAME_FILE) as f:
        channels = json.load(f)

    m3u_content = ["#EXTM3U"]
    
    for channel in channels:
        print(f"Processing: {channel['name']}")
        channel_id = get_channel_id(channel["username"].lstrip("@"))
        video_id = get_live_video_id(channel_id) if channel_id else None
        
        if video_id:
            m3u_content.append(
                f'#EXTINF:-1 tvg-logo="{channel["logo"]}",{channel["name"]}\n'
                f'https://m.xigzo.store/yt/live.php?video_id={video_id}'
            )

    m3u_content.append(f"\n# Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    with open(PLAYLIST_FILE, "w") as f:
        f.write("\n".join(m3u_content))

if __name__ == "__main__":
    generate_playlist()
