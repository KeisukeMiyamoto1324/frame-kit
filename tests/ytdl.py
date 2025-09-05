# PYTHONPATH=$(pwd)/src python3 -m tests.ytdl

from pytubefix import YouTube
from pytubefix.cli import on_progress

url = "https://www.youtube.com/watch?v=eOeLO8NeRb0"

yt = YouTube(url, on_progress_callback=on_progress)
print(yt.title)

ys = yt.streams.get_audio_only()
ys.download()
