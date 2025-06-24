# YouTube Downloader

A Python application that allows you to download YouTube videos as MP3 files with metadata (artist name and thumbnail) embedded. The application features a graphical user interface built with PyQt6.

## Features

- Download YouTube videos as high-quality MP3 files (320kbps)
- Automatically extract and embed metadata:
  - Artist name (parsed from video title or channel name)
  - Thumbnail image as album art
- Search YouTube directly from the application
- Add downloaded songs to Apple Music (macOS only)
- Modern and user-friendly GUI interface

## Requirements

- Python 3.8 or higher
- FFmpeg (required for audio conversion)
- macOS (for Apple Music integration)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd youtube-downloader
   ```

2. Install FFmpeg (if not already installed):
   - On macOS (using Homebrew):
     ```bash
     brew install ffmpeg
     ```
   - On Ubuntu/Debian:
     ```bash
     sudo apt-get install ffmpeg
     ```
   - On Windows:
     Download from [FFmpeg website](https://ffmpeg.org/download.html)

3. Install the package and its dependencies:
   ```bash
   pip install -e .
   ```

## Usage

### Running the Application

1. Start the application:
   ```bash
   python -m youtube_downloader
   ```

2. Using the GUI:
   - Enter a YouTube URL in the input field
   - Click "Download" to start the download
   - The downloaded MP3 will be saved in the `downloads` directory
   - On macOS, you can optionally add the downloaded songs to Apple Music

### Command Line Usage

The application can also be used from the command line:

1. Search for a video:
   ```bash
   python -m youtube_downloader.search "song name"
   ```

2. Download a video:
   ```bash
   python -m youtube_downloader.download "youtube-url"
   ```

## Project Structure

```
youtube_downloader/
├── __init__.py
├── __main__.py
├── core/
│   ├── __init__.py
│   ├── downloader.py
│   └── metadata.py
├── gui/
│   ├── __init__.py
│   └── main_window.py
├── utils/
│   ├── __init__.py
│   └── apple_music.py
└── workers/
    ├── __init__.py
    └── download_worker.py
```

## Development

To set up the development environment:

1. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

2. Run tests (if available):
   ```bash
   pytest
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube video downloading
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework
- [mutagen](https://mutagen.readthedocs.io/) for MP3 metadata handling 