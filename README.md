<div align="center">

  <img src="docs/logo.png" alt="Rivra Logo" width="130" />

# Rivra

**A modern, fast, and intuitive multimedia downloader for Windows**<br>
Built with Python, CustomTkinter, and the power of [yt-dlp](https://github.com/yt-dlp/yt-dlp).

  <p>
    <a href="https://github.com/blnkDev/Yt-Downloader/releases/latest">
      <img src="https://img.shields.io/badge/Download-Windows%20(.exe)-0078D4?style=for-the-badge&logo=windows&logoColor=white" alt="Download Windows" />
    </a>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+" />
    <img src="https://img.shields.io/badge/GUI-CustomTkinter-2B2B2B?style=flat-square" alt="CustomTkinter" />
    <img src="https://img.shields.io/badge/Engine-yt--dlp-FF0000?style=flat-square" alt="yt-dlp" />
    <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" alt="License MIT" />
  </p>

</div>

---

## 📖 Overview

**Rivra** is a Windows desktop application designed to download videos and audio from **1,000+ platforms** with ease, speed, and a modern Dark Mode interface.

No terminal commands. No complicated configuration. Just paste a link and download.

---

## 📸 Interface Preview

---

## 📦 Download & Usage

If you just want to use Rivra without installing Python or any dependencies:

1. Go to the [**Releases**](https://github.com/blnkDev/Yt-Downloader/releases) page.
2. Download the latest version (`Rivra.exe` or `Rivra.zip`).
3. Run the application and start downloading!

---

## ✨ Features

* **High-Quality Video (MP4):** Up to 1080p Full HD with integrated audio (H.264 + AAC).
* **Audio Extraction (MP3):** Choose between 128 kbps, 192 kbps, and 320 kbps.
* **Instant Preview:** Automatically loads the thumbnail, title, channel, and duration as soon as a link is entered.
* **Automatic Link Detection:** When you focus the app with a copied link, Rivra automatically detects, pastes, and analyzes it.
* **Playlist Support:** Detects and downloads complete playlists, automatically organizing files into folders.
* **Embedded Metadata & Cover Art:** Automatically embeds album artwork and ID3 tags into media files using FFmpeg.
* **Accelerated Downloads:** Uses up to 8 concurrent connections for faster downloads.
* **Automatic yt-dlp Updates:** Checks for engine updates on startup and lets you update with a single click.
* **Persistent Download Folder:** Remembers your preferred destination folder between sessions.
* **Safe Cancellation:** Cancel downloads at any time without freezing the application.
* **Asynchronous Processing:** Downloads and media processing run in the background, keeping the interface responsive.

---

## 🌐 Supported Platforms

Rivra supports **1,000+ websites** through the `yt-dlp` engine.

Some of the most popular platforms include:

| Platform                                | Video | Audio |
| --------------------------------------- | :---: | :---: |
| **YouTube** (Videos, Shorts, Playlists) |  Yes  |  Yes  |
| **TikTok**                              |  Yes  |  Yes  |
| **Instagram** (Reels, Posts)            |  Yes  |  Yes  |
| **X / Twitter**                         |  Yes  |  Yes  |
| **SoundCloud**                          |   —   |  Yes  |
| **Vimeo**                               |  Yes  |  Yes  |
| **Twitch** (Clips, VODs)                |  Yes  |  Yes  |
| **Facebook**                            |  Yes  |  Yes  |

> **Note:** Actual availability may vary depending on the platform and its current restrictions. Rivra relies on `yt-dlp` for platform support.

---

## 🛠️ Built With

| Component             | Technology                                                | Purpose                                                  |
| --------------------- | --------------------------------------------------------- | -------------------------------------------------------- |
| **GUI**               | [CustomTkinter](https://customtkinter.tomschimansky.com/) | Modern and responsive Dark Mode interface                |
| **Extraction Engine** | [yt-dlp](https://github.com/yt-dlp/yt-dlp)                | Multimedia extraction and downloading                    |
| **Media Processing**  | [FFmpeg](https://ffmpeg.org/)                             | Stream muxing, audio conversion, and cover art embedding |
| **Image Processing**  | [Pillow](https://pypi.org/project/Pillow/)                | Thumbnail and artwork rendering                          |
| **HTTP Requests**     | [Requests](https://pypi.org/project/requests/)            | Cover downloads and version checks                       |
| **Packaging**         | [PyInstaller](https://pyinstaller.org/)                   | Standalone executable generation                         |

---

## 💻 Running from Source

### Requirements

* Python 3.10 or newer
* FFmpeg binaries inside the `ffmpeg/` directory

```bash
# 1. Clone the repository
git clone https://github.com/blnkDev/Yt-Downloader.git
cd Yt-Downloader

# 2. Create and activate a virtual environment (optional)
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the application
python baixador.py
```

---

## 🔨 Building the Executable

To build your own Windows executable:

```bash
pip install pyinstaller
python -m PyInstaller --clean baixador.spec
```

The generated executable will be located at:

```text
dist/baixador.exe
```

---

## 📁 Project Structure

```text
Rivra/
├── docs/
│   └── logo.png
├── ffmpeg/
│   └── ...
├── baixador.py
├── baixador.spec
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 📄 License

Rivra is distributed under the **MIT License**.

See the [LICENSE](LICENSE) file for more details.

---

<div align="center">

**Rivra — Free. Fast. Simple.**

</div>
