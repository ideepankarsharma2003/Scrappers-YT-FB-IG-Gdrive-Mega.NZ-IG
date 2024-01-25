from bs4 import BeautifulSoup
from selenium import webdriver
from uuid import uuid4
import re
import requests


import os
PATH = "research/edge drivers/msedgedriver"



reg1= '"mime_type":"audio\\\\/mp4","codecs":"[^"]+","base_url":"[^"]+'
reg2= '"mime_type":"audio\\\\/mp4","codecs":"[^"]+","base_url":"'



def extract_url_from_source(html_content: str):
    base_url= ""
    print(type(html_content))
    
    soup= BeautifulSoup(html_content, "html.parser")
    
    for script in soup.body.find_all("script"):
        contents= script.contents
        if len(contents)>0:
            reg1_test= re.search(reg1, contents[0])
            if reg1_test:
                base_url_match= contents[0][reg1_test.start():reg1_test.end()]
                url= re.search(reg2, base_url_match)
                base_url= base_url_match[url.end():].replace('\\','')
                print(f"base url: {base_url}")
                return base_url
            
            


headers= {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 \
    Safari/537.36 Edg/79.0.309.43",
    # "cookie": f'sessionid={SESSIONID};'
}           
def extract_video_from_url(url:str):
    driver= webdriver.Edge(PATH)
    
    driver.get(url)
    page_source = driver.page_source
    base_url= extract_url_from_source(page_source)
    # driver.get(base_url)
    
    response= requests.get(base_url, headers=headers)
    
    if response.status_code == 200:
        filename= f"dummy_clips/{uuid4().__str__()}.mp4"
        with open(filename, "wb") as f:
            f.write(
                response.content
            )
            
    return filename
    
    
            
            
            
            

            
            