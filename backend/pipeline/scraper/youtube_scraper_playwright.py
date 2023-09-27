from selectolax.parser import HTMLParser
from playwright.async_api import async_playwright



TIMEOUT = 30000
# # Scrape the first video url and title
# async def scrape_first_video_link_and_title():
#     domain = "https://www.youtube.com"
#     url = "https://www.youtube.com/@hubermanlab/videos"
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)

#         page = await browser.new_page()
#         await page.goto(url)

#         content = await page.content()
#         tree = HTMLParser(content)

#         newest_video = tree.css_first("a#video-title-link")
#         url = newest_video.attrs.get('href')
#         title = newest_video.text()
#         await browser.close()
#     return {"url": domain + url, "title": title}

# Go to the url and scrape the transcript
async def scrape_video_transcript(url=""):
    """Wait for the transcript loaded, and the return the video page body"""
    
    # Remove this later when there is transcript available
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        page = await browser.new_page()
        await page.goto(url)
        description_selector = "#description-inner"
        no_thanks_selector = "#dismiss-button > yt-button-renderer > yt-button-shape > button > yt-touch-feedback-shape > div > div.yt-spec-touch-feedback-shape__fill"
        transcript_btn_selector = "#description-inner [aria-label='Show transcript']"
        transcript_elements = "yt-formatted-string.segment-text.style-scope.ytd-transcript-segment-renderer"
        
        print("waiting for no thank button...")
        # Sometimes the no thanks button won't appear
        try:
            await page.wait_for_selector(no_thanks_selector, timeout=10000)
            await page.click(no_thanks_selector)
        except Exception as e:
            print(e)
            print("no thank button did not appear...")

        # Click the description, because the transcripts button are now moved to description
        await page.click(description_selector)
        print("Description button clicked")
        try:
            await page.wait_for_selector(transcript_btn_selector, timeout=TIMEOUT)
        except TimeoutError: 
            print("Wait for transcripts button but got timeout")
            return 

        await page.click(transcript_btn_selector)
        print("Transcript button clicked")

        # wait for transcripts loaded
        
        await page.wait_for_selector(transcript_elements, timeout=TIMEOUT)
        

        # Grab the html body tree
        content = await page.content()
        tree = HTMLParser(content)
        
        await browser.close()
        return tree


async def start_scrape(url):

    # # Get the first video url
    # data = await scrape_first_video_link_and_title(url)

    # title = data['title']
    # url = data['url']

    # Go in the url, render it and get contents of the page
    tree = await scrape_video_transcript(url)

    # Extract the title
    title = tree.css_first("#title h1").text()
    
    # Extract transcripts from content
    transcript_tags = tree.css("yt-formatted-string.segment-text.style-scope.ytd-transcript-segment-renderer")
    
    
    # Save it as txt file
    transcripts = ""
    for tag in transcript_tags:
        transcripts += f"{tag.text()}\n"
    
    with open("video_transcripts.txt", "w",encoding="utf-8") as f:
        f.write(transcripts)

    # Return the text
    return {"transcript": transcripts, "url": url, "title": title}


if __name__=='__main__':
    # asyncio.run(start_scrape())
   
    pass

