import streamlit as st
from utils.downloader import download_youtube_video
import os


url= st.text_input("Enter the link to youtube video")
b1= st.button("Convert video")

if b1:
    audiofile, videofile= download_youtube_video(url)
    if os.path.exists(audiofile):
        st.audio(audiofile, format="audio/mp3")
        os.remove(audiofile)
        os.remove(videofile) # mp4 video file