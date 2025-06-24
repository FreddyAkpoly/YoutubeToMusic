from setuptools import setup, find_packages

setup(
    name="youtube_downloader",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'PyQt6',
        'yt-dlp',
        'Pillow',
        'mutagen',
        'requests'
    ],
    extras_require={
        'dev': [
            'pyinstaller',
        ],
    },
    entry_points={
        'console_scripts': [
            'youtube_downloader=youtube_downloader.__main__:main',
        ],
    },
) 