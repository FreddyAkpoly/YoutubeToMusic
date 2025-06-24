import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QLineEdit, QLabel, QFileDialog,
                           QTextEdit, QTabWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import requests
from PIL import Image
from io import BytesIO

from ..workers.search_worker import SearchWorker
from ..workers.download_worker import DownloadWorker
from ..utils.queue_manager import QueueManager

class YouTubeDownloaderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Music Downloader")
        self.setMinimumSize(800, 600)
        
        # Initialize queue manager
        self.queue_manager = QueueManager()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create tabs
        tabs = QTabWidget()
        search_tab = QWidget()
        url_tab = QWidget()
        tabs.addTab(search_tab, "Search Songs")
        tabs.addTab(url_tab, "Direct URLs")
        layout.addWidget(tabs)
        
        # Set up Search tab
        self.setup_search_tab(search_tab)
        
        # Set up URL tab
        self.setup_url_tab(url_tab)
        
        # Common sections
        self.setup_common_sections(layout)
        
        # Initialize workers
        self.worker = None
        self.search_worker = None
        self.current_search_result = None

    def setup_search_tab(self, tab):
        search_layout = QVBoxLayout(tab)
        
        # Search input section
        search_input_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter song name to search...")
        self.search_input.returnPressed.connect(self.search_song)
        search_input_layout.addWidget(self.search_input)
        
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_song)
        search_input_layout.addWidget(self.search_button)
        search_layout.addLayout(search_input_layout)
        
        # Search results section with thumbnail
        results_layout = QHBoxLayout()
        
        # Thumbnail section
        thumbnail_layout = QVBoxLayout()
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(200, 200)
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail_label.setStyleSheet("border: 1px solid #ccc; background-color: #f0f0f0;")
        thumbnail_layout.addWidget(self.thumbnail_label)
        results_layout.addLayout(thumbnail_layout)
        
        # Text results section
        results_text_layout = QVBoxLayout()
        self.search_results = QTextEdit()
        self.search_results.setReadOnly(True)
        self.search_results.setPlaceholderText("Search results will appear here...")
        self.search_results.setMaximumHeight(200)
        results_text_layout.addWidget(self.search_results)
        
        # Add to download list button
        self.add_to_list_button = QPushButton("Add to Download List")
        self.add_to_list_button.clicked.connect(self.add_search_result)
        self.add_to_list_button.setEnabled(False)
        results_text_layout.addWidget(self.add_to_list_button)
        
        results_layout.addLayout(results_text_layout)
        search_layout.addLayout(results_layout)

    def setup_url_tab(self, tab):
        url_layout = QVBoxLayout(tab)
        
        # URL input section
        url_input_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube URL")
        url_input_layout.addWidget(self.url_input)
        
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_url)
        url_input_layout.addWidget(self.add_button)
        url_layout.addLayout(url_input_layout)

    def setup_common_sections(self, layout):
        # Download list section
        download_list_label = QLabel("Download Queue:")
        layout.addWidget(download_list_label)
        
        self.urls_list = QTextEdit()
        self.urls_list.setPlaceholderText("URLs to download will appear here...")
        # Load saved queue
        queue = self.queue_manager.get_queue()
        if queue:
            self.urls_list.setText("\n".join(queue))
        layout.addWidget(self.urls_list)
        
        # Save location section
        save_layout = QHBoxLayout()
        save_label = QLabel("Save Location:")
        save_layout.addWidget(save_label)
        
        self.save_path = QLineEdit()
        self.save_path.setText(os.path.join(os.getcwd(), "downloads"))
        save_layout.addWidget(self.save_path)
        
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_location)
        save_layout.addWidget(browse_button)
        layout.addLayout(save_layout)
        
        # Progress section
        progress_label = QLabel("Progress:")
        layout.addWidget(progress_label)
        
        self.progress_text = QTextEdit()
        self.progress_text.setReadOnly(True)
        self.progress_text.setMaximumHeight(100)
        layout.addWidget(self.progress_text)
        
        # Download button
        self.download_button = QPushButton("Download All")
        self.download_button.clicked.connect(self.start_download)
        self.download_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(self.download_button)

    def search_song(self):
        query = self.search_input.text().strip()
        if not query:
            return
            
        self.search_button.setEnabled(False)
        self.search_results.clear()
        self.search_results.append("Searching...")
        self.current_search_result = None
        self.add_to_list_button.setEnabled(False)
        
        self.search_worker = SearchWorker(query)
        self.search_worker.result.connect(self.handle_search_result)
        self.search_worker.error.connect(self.handle_search_error)
        self.search_worker.finished.connect(lambda: self.search_button.setEnabled(True))
        self.search_worker.start()

    def handle_search_result(self, url, title, thumbnail_url):
        self.search_results.clear()
        self.search_results.append(f"Found: {title}\nURL: {url}")
        self.current_search_result = url
        self.add_to_list_button.setEnabled(True)
        
        # Display thumbnail
        try:
            response = requests.get(thumbnail_url)
            image = Image.open(BytesIO(response.content))
            image = image.convert("RGB")
            
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            
            pixmap = QPixmap()
            pixmap.loadFromData(img_byte_arr)
            pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            
            self.thumbnail_label.setPixmap(pixmap)
        except Exception as e:
            print(f"Error loading thumbnail: {e}")
            self.thumbnail_label.clear()
            self.thumbnail_label.setText("No thumbnail")

    def handle_search_error(self, error_message):
        self.search_results.clear()
        self.search_results.append(f"Error: {error_message}")
        self.current_search_result = None
        self.add_to_list_button.setEnabled(False)
        self.thumbnail_label.clear()
        self.thumbnail_label.setText("No thumbnail")

    def add_search_result(self):
        if self.current_search_result:
            current_text = self.urls_list.toPlainText()
            if current_text:
                self.urls_list.append(f"\n{self.current_search_result}")
            else:
                self.urls_list.setText(self.current_search_result)
            self.search_input.clear()
            self.search_results.clear()
            self.thumbnail_label.clear()
            self.current_search_result = None
            self.add_to_list_button.setEnabled(False)
            self.update_queue()

    def add_url(self):
        url = self.url_input.text().strip()
        if url:
            current_text = self.urls_list.toPlainText()
            if current_text:
                self.urls_list.append(f"\n{url}")
            else:
                self.urls_list.setText(url)
            self.url_input.clear()
            self.update_queue()

    def update_queue(self):
        """Update the queue with current URLs"""
        urls = self.urls_list.toPlainText().strip().split('\n')
        self.queue_manager.update_queue(urls)

    def browse_location(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Save Location")
        if folder:
            self.save_path.setText(folder)

    def start_download(self):
        urls = self.urls_list.toPlainText().split("\n")
        save_path = self.save_path.text()
        
        if not urls or not urls[0].strip():
            self.progress_text.append("Please add at least one URL!")
            return
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        self.download_button.setEnabled(False)
        self.worker = DownloadWorker(urls, save_path)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.download_finished)
        self.worker.start()

    def update_progress(self, message):
        self.progress_text.append(message)

    def download_finished(self):
        self.download_button.setEnabled(True)
        self.urls_list.clear()
        self.queue_manager.clear_queue()

    def closeEvent(self, event):
        """Override close event to save queue before closing"""
        self.update_queue()
        super().closeEvent(event) 