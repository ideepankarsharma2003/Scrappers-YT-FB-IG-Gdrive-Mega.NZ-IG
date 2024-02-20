import re
import os
import time
import requests
from tqdm import tqdm
from playwright.sync_api import Playwright, sync_playwright, expect
import argparse
parser = argparse.ArgumentParser(description ='Argument Parser')


parser.add_argument(
    "-V", "--video", help="URL of the youtube video", required=True
)


parser.add_argument(
    "-F", "--filename", help="Filename of the blackboxai txt", required=True
)

args = parser.parse_args()


r1= "https:\/\/youtu\.be\/[^?]+"
r2= "https:\/\/youtu\.be\/"

def input_url_2_actual_url(url):
    base_url= re.search(r1, url)[0] 
    id= re.split(r2, base_url)[1]
    return f"https://www.youtube.com/watch?v={id}"




video_url= args.video
if re.match(r1, video_url):
    video_url = input_url_2_actual_url(video_url)

filename= os.path.splitext(args.filename)[0]
filename= f"{filename}_blackboxai.txt"


print(f"""
      filename: {filename}
      video_url: {video_url}
      """)



def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.blackbox.ai/")
    page.locator("div").filter(has_text=re.compile(r"^Youtube$")).click()
    page.get_by_placeholder("Ask Any Question...").click()
    page.get_by_placeholder("Ask Any Question...").fill(video_url)
    page.get_by_role("button", name="Send message").click()
    
    # print(page.get_by_placeholder("Is this conversation helpful so far?"))
    print("\n[Going to Sleep for 60 seconds]\n".upper())
    for i in tqdm(range(60)):
        time.sleep(1)
    print("\n[Finished Sleep for 60 seconds]\n".upper())
    

    print("Saving Page Content: ")
    # page_content= page.locator("div:nth-child(2) > .group > .ml-4").text_content()
    page_content= page.locator("div:nth-child(2) > .group > .ml-4").inner_html()
    
    with open(filename, "w") as f:
        f.write(page_content)
        
    # ---------------------
    # page.get_by_role("button", name="Copy Link to Share Chat").click()
    # print(
        
    # )
    context.close()
    browser.close()
with sync_playwright() as playwright:
    run(playwright)
