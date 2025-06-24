import os
import subprocess
from yt_dlp import YoutubeDL
import requests
from PIL import Image
from io import BytesIO
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TPE1

def get_metadata_from_url(url, save_path):
    with YoutubeDL({'quiet': True}) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict['title']
        uploader = info_dict.get('uploader', 'Unknown Uploader')
        thumbnail_url = info_dict.get('thumbnail')

        if "-" in title:
            artist = title.split("-")[0].strip()
        else:
            artist = uploader

        file_name = f"{save_path}/{title}.mp3"
        return file_name, title, artist, thumbnail_url

def download_audio_as_mp3(url, save_path):
    file_name, title, artist, thumbnail_url = get_metadata_from_url(url, save_path)
    
    if os.path.exists(file_name):
        print(f"Skipping {file_name} (already exists).")
        return

    options = {
        'format': 'bestaudio/best',
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'noplaylist': True,
    }

    with YoutubeDL(options) as ydl:
        ydl.download([url])
        embed_metadata_in_mp3(file_name, thumbnail_url, artist)

def embed_metadata_in_mp3(mp3_file, thumbnail_url, artist):
    try:
        audio = MP3(mp3_file, ID3=ID3)
        
        audio.tags.add(TPE1(encoding=3, text=artist))

        if thumbnail_url:
            response = requests.get(thumbnail_url)
            image = Image.open(BytesIO(response.content))

            thumbnail_path = mp3_file.replace('.mp3', '.jpg')
            image.save(thumbnail_path)

            with open(thumbnail_path, 'rb') as img_file:
                audio.tags.add(APIC(
                    encoding=3,
                    mime='image/jpeg',
                    type=3,
                    desc='Cover',
                    data=img_file.read()
                ))
            os.remove(thumbnail_path)

        audio.save()
    except Exception as e:
        print(f"Error embedding metadata: {e}")

def add_to_apple_music():
    try:
        subprocess.run(["osascript", "/Users/freddyakpoly/Documents/AddToAppleMusic.scpt"])
        print("Songs added to Apple Music.")
    except Exception as e:
        print(f"Error adding songs to Apple Music: {e}") 