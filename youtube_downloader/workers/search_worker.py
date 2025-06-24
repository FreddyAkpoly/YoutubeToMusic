from PyQt6.QtCore import QThread, pyqtSignal
from yt_dlp import YoutubeDL

class SearchWorker(QThread):
    result = pyqtSignal(str, str, str)  # signals: url, title, thumbnail_url
    error = pyqtSignal(str)

    def __init__(self, query):
        super().__init__()
        self.query = query

    def run(self):
        try:
            with YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(f"ytsearch1:{self.query}", download=False)
                if info and 'entries' in info and info['entries']:
                    video = info['entries'][0]
                    url = f"https://www.youtube.com/watch?v={video['id']}"
                    title = video['title']
                    thumbnail_url = video.get('thumbnail', '')
                    self.result.emit(url, title, thumbnail_url)
                else:
                    self.error.emit("No results found")
        except Exception as e:
            self.error.emit(f"Error during search: {str(e)}") 