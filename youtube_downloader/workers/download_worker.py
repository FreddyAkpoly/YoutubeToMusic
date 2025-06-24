from PyQt6.QtCore import QThread, pyqtSignal
from ..core.downloader import download_audio_as_mp3, add_to_apple_music

class DownloadWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, urls, save_path):
        super().__init__()
        self.urls = urls
        self.save_path = save_path

    def run(self):
        for url in self.urls:
            if url.strip():
                self.progress.emit(f"Downloading: {url}")
                try:
                    download_audio_as_mp3(url.strip(), self.save_path)
                    self.progress.emit(f"Successfully downloaded: {url}")
                except Exception as e:
                    self.progress.emit(f"Error downloading {url}: {str(e)}")
        
        self.progress.emit("All downloads completed!")
        try:
            add_to_apple_music()
            self.progress.emit("Songs added to Apple Music!")
        except Exception as e:
            self.progress.emit(f"Error adding to Apple Music: {str(e)}")
        self.finished.emit() 