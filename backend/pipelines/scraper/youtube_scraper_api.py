from youtube_transcript_api import YouTubeTranscriptApi
from youtube_search import YoutubeSearch

def get_youtube_transcript(video_id):
    
    try:
        res = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    except Exception as e:
        print("Failed to get YouTube transcript through API")
        print(e)
        return 
    
    transcript = ""
    for t in res:
        transcript += f"{t['text']}\n"
        
    return transcript

def get_youtube_video_data(query):
    # Get youtube data using query
    try:
        result = YoutubeSearch(query, max_results=1).to_dict()
    except Exception as e:
        print("Failed to get YouTube video data through API")
        print(e)
        return {"status": "failed"}
    video = result[0]
    video_id = video["id"]
    title = video["title"]
    channel_name = video["channel"]
    url_suffix = video["url_suffix"]
    url = "https://www.youtube.com" + url_suffix
    
    data = {
        "status": "success",
        "video_id": video_id,
        "title": title,
        "url": url,
        "channel_name": channel_name
    }
    return data