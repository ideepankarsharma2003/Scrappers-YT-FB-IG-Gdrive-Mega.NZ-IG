import re
from playwright.sync_api import sync_playwright
import requests







r = "https:\/\/scontent\.cdninstagram\.com\/v\/[^\/]+\/[^/.]+.mp4\?"
compiled_regex = re.compile(r)
print(f"regex: {compiled_regex}")
class PlaywrightManager:
    def __enter__(self):
        self.playwright = sync_playwright().start()
        return self.playwright
    def __exit__(self, exc_type, exc_value, traceback):
        self.playwright.stop()
def extract_igvideo_from_url(url, mp4_filename):
    url = url.replace("reels", "reel").split("?")[0]
    with PlaywrightManager() as playwright:
        browser = playwright.chromium.launch(headless=True, channel="msedge")
        page = browser.new_page()
        url_found = False
        file_downloaded = False
        def print_response_url(response):
            nonlocal url_found, file_downloaded
            if file_downloaded:
                return  # Skip further processing if the file is already downloaded
            if ".mp4" in response.url:
                print(f"url: {response.url}")
                video_url = response.url
                with open(mp4_filename, "wb") as f:
                    video = requests.get(video_url)
                    f.write(video.content)
                    print("[FILE DOWNLOADED]\n")
                    url_found = True
                    file_downloaded = True
            else:
                print("USELESS URL RESPONSE")
        # For every response trigger this
        page.on("response", print_response_url)
        # Enable network events tracking
        try:
            with page.expect_response(compiled_regex) as response_info:
                page.goto(url)
            print(f"response_info: {response_info}")
        except Exception as e:
            print(e)
            print("Closed by exception")
            return None
        if url_found:
            browser.close()
            print("Browser is stopped after finding the URL.")
            return
        
        
url = "https://www.instagram.com/reels/C3iDCCgvY8U/"
print(extract_igvideo_from_url(url, "video.mp4"))
