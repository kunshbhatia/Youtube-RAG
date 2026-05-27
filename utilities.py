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