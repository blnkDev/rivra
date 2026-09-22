# Rivra

> A fast, modern media downloader for Windows — powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp).

<!-- Replace with your logo once available -->
<!-- <p align="center"><img src="docs/logo.png" alt="Rivra logo" width="180" /></p> -->

---

## Overview

Rivra is a desktop application that lets you download videos and audio from over 1,000 platforms — YouTube, TikTok, Instagram, X/Twitter, SoundCloud, Vimeo, and more — through a clean, dark-mode interface. No terminal required.

## Features

| | |
|---|---|
| Video | MP4 up to 1080p Full HD (H.264 + AAC) |
| Audio | MP3 at 128 / 192 / 320 kbps |
| Platforms | YouTube, TikTok, Instagram Reels, X/Twitter, SoundCloud, Vimeo, Twitch, Facebook and 1,000+ more |
| Preview | Thumbnail, title, channel and duration loaded automatically when you paste a link |
| Auto-paste | Detects a copied link when the window gains focus |
| Playlists | Detects and downloads full playlists into organized subfolders |
| Metadata | Embeds cover art and ID3 tags into every MP3 and MP4 |
| Speed | Up to 8 concurrent fragments and 10 MB chunks |
| Updates | Checks for yt-dlp updates on startup and installs them in the background |
| Persistence | Remembers your last destination folder between sessions |

## Tech Stack

| Package | Role |
|---|---|
| [Python 3.12](https://www.python.org/) | Runtime |
| [CustomTkinter](https://customtkinter.tomschimansky.com/) | Dark-mode GUI |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Download engine |
| [FFmpeg](https://ffmpeg.org/) | Media processing & muxing |
| [Pillow](https://pypi.org/project/Pillow/) | Thumbnail rendering |
| [Requests](https://pypi.org/project/requests/) | HTTP (thumbnails, update checks) |
| [PyInstaller](https://pyinstaller.org/) | Standalone executable |

---

## Running from source

**Requirements:** Python 3.10+, FFmpeg binaries inside `ffmpeg/`

```bash
git clone https://github.com/blnkDev/Yt-Downloader.git
cd Yt-Downloader

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
python baixador.py
```

## Building the executable

```bash
pip install pyinstaller
python -m PyInstaller --clean baixador.spec
# Output: dist/baixador.exe
```

---

## Contributing

Issues and pull requests are welcome.

## License

MIT — see [LICENSE](LICENSE) for details.
