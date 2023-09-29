from pipelines.scraper.youtube_scraper_api import get_youtube_transcript
from pipelines.summarizer.summary import start_summarize
import time 


def summary_pipeline(url, title, video_id, channel_name):
    
    print(f"This is the video title to scrape:\n{title}")
    print(f"This is the video url to scrape:\n{url}")
    print()
    # Real-time scrape the video data
    start = time.time()
    
    print("Start scraping the video transcript...")
    
    # Get transcripts through youtube api 
    transcript = get_youtube_transcript(video_id=video_id)
    
    if transcript is None:
        return {"status": "failed", "issue_source": "transcript"}

    print("Scraping transcript done!")
    print()
    
    # Summarize the transcript
    print("Start summary process...")
    
    short_full_summary = start_summarize(
        text=transcript, 
        title=title, 
        url=url, 
        channel_name=channel_name
    )

    end = time.time()
    time_spent = end - start
    print(f"Time total time spent on summary: {round(time_spent, 2)} seconds")
    
    return {"status": "success", "summary": short_full_summary}
    