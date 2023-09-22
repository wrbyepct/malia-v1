from selectolax.parser import HTMLParser
from playwright.async_api import async_playwright



TIMEOUT = 30000
# Scrape the first video url and title
async def scrape_first_video_link_and_title():
    domain = "https://www.youtube.com"
    url = "https://www.youtube.com/@hubermanlab/videos"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        page = await browser.new_page()
        await page.goto(url)

        content = await page.content()
        tree = HTMLParser(content)

        newest_video = tree.css_first("a#video-title-link")
        url = newest_video.attrs.get('href')
        title = newest_video.text()
        await browser.close()
    return {"url": domain + url, "title": title}

# Go to the url and scrape the transcript
async def scrape_video_transcript(url=""):
    # Remove this later when there is transcript available
    url = "https://www.youtube.com/watch?v=yixIc1Ai6jM"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        page = await browser.new_page()
        await page.goto(url)
        no_thanks_selector = "#dismiss-button > yt-button-renderer > yt-button-shape > button > yt-touch-feedback-shape > div > div.yt-spec-touch-feedback-shape__fill"
        float_menu_selector = "#button-shape > button > yt-touch-feedback-shape > div > div.yt-spec-touch-feedback-shape__fill"
        transcript_btn_selector = "#items > ytd-menu-service-item-renderer > tp-yt-paper-item"
        transcript_elements = "yt-formatted-string.segment-text.style-scope.ytd-transcript-segment-renderer"

        print("waiting for no thank button...")
        # Sometimes the no thanks button won't appear
        try:
            await page.wait_for_selector(no_thanks_selector, timeout=10000)
            await page.click(no_thanks_selector)
        except Exception as e:
            print(e)
            print("no thank button did not appear...")

        await page.click(float_menu_selector)

        await page.wait_for_selector(transcript_btn_selector, timeout=TIMEOUT)

        await page.click(transcript_btn_selector)
        

        # wait for transcripts loaded
        await page.wait_for_selector(transcript_elements, timeout=TIMEOUT)

        # Grab the html body tree
        content = await page.content()
        tree = HTMLParser(content)
        
        await browser.close()
        return tree


async def start_scrape():

    # Get the first video url
    data = await scrape_first_video_link_and_title()

    title = data['title']
    url = data['url']

    # Go in the url, render it and get contents of the page
    tree = await scrape_video_transcript(url)

    # Extract transcripts from content
    transcript_tags = tree.css("yt-formatted-string.segment-text.style-scope.ytd-transcript-segment-renderer")

    # Save it as txt file
    transcripts = ""
    for tag in transcript_tags:
        transcripts += f"{tag.text()}\n"
    
    with open("huberman_transcripts.txt", "w",encoding="utf-8") as f:
        f.write(transcripts)

    # Return the text
    return {"transcript": transcripts, "url": url, "title": title}


if __name__=='__main__':
    # asyncio.run(start_scrape())
   
    pass

