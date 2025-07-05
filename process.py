import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("YT_API_KEY")
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
                f'https://youtube.com/watch?v={video_id}'
            )

    m3u_content.append(f"\n# Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    m3u_content.append("# Generated with YouTube Live Playlist Generator")
    
    with open(PLAYLIST_FILE, "w", encoding='utf-8') as f:
        f.write("\n".join(m3u_content))

if __name__ == "__main__":
    generate_playlist()
