from uuid import uuid4
import moviepy.editor as mp
from pytube import YouTube 




def generate_audio(input_file:str, output_file:str):
    clip= mp.VideoFileClip(input_file)
    clip.audio.write_audiofile(output_file)
    
    
def download_youtube_video(url: str):
    try:
        file= uuid4().hex
        SAVE_PATH= "dummy_vids/"
        input_file= f"dummy_vids/{file}.mp4"
        output_file= f"dummy_clips/{file}.mp3"
        yt = YouTube(url)  
        yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().last().download(SAVE_PATH, filename=f"{file}.mp4")
        generate_audio(input_file, output_file)
        return output_file, input_file
    except Exception as e:
        return e.__str__(), ""
    