from pytube import YouTube
import os
from moviepy.editor import *

# Pfad zum Download-Ordner
download_folder = "./downloads"

# erstelle Download-Ordner, wenn er nicht vorhanden ist
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Liste der YouTube-Links aus Datei lesen
with open("output.txt", "r") as file:
    links = file.read().splitlines()

# Schleife durch die Links und lade jedes Video herunter
for link in links:
    try:
        yt = YouTube(link)

        # Wähle das Video mit der höchsten Auflösung aus
        stream = yt.streams.get_highest_resolution()

        # Video herunterladen
        stream.download(download_folder)

        # Video konvertieren
        video_path = os.path.join(download_folder, stream.default_filename)
        audio_path = os.path.join(download_folder, f"{yt.title}.mp3")
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path)

        # Video-Datei löschen
        os.remove(video_path)

        print(f"Video {yt.title} erfolgreich heruntergeladen und konvertiert!")
    except:
        print(f"Fehler beim Herunterladen oder Konvertieren von {link}.")
