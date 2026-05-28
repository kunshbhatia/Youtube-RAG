import re
import yt_dlp


def get_video_details(url):

    ydl_opts = {"quiet": True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(url, download=False)

        title = info.get("title")
        description = info.get("description")
        channel = info.get("channel")
        views = info.get("view_count")
        duration = info.get("duration")
        thumbnail = info.get("thumbnail")

        return title,description,channel,views,duration,thumbnail
    
#Made by Kunsh Bhatia


def extract_video_id(youtube_url): #Extract the video ID from a YouTube URL.

    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',  # Standard and shortened URLs
        r'(?:embed\/)([0-9A-Za-z_-]{11})',   # Embed URLs
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'  # youtu.be URLs
    ]
    
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    
    return None