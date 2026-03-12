<div align="center">

# 🎧 LofiGurl

**A tiny, always-on-top lofi radio player for Windows**  
*Streams lofi hip hop radio — beats to relax/study to, straight to your desktop.*

![Python](https://img.shields.io/badge/Python-3.8%2B-c9a96e?style=flat-square&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-c9a96e?style=flat-square&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-c9a96e?style=flat-square)
![Made with ❤️](https://img.shields.io/badge/Made%20by-corazonthedev-c9a96e?style=flat-square)

</div>

---

## ✨ Features

- 🎵 **Live stream** — plays the [lofi girl 24/7 radio](https://www.youtube.com/watch?v=jfKfPfyJRdk) via yt-dlp + ffmpeg
- 🖼️ **Custom frameless UI** — dark aesthetic with a hand-drawn lofi girl illustration
- 📌 **Always on top** — stays above your other windows while you work or study
- 🔊 **Volume control** — click the bar or use `+` / `−` buttons
- ⏸️ **Play / Pause** — toggle the stream at any time
- 🕐 **Session timer** — shows how long you've been listening
- 🗂️ **System tray minimize** — hides to hidden icons, not the taskbar
- 🖱️ **Draggable** — click and drag anywhere to reposition
- 🔗 **Made by corazonthedev** — clickable link in the footer
- 🎨 **Lofi Girl .ico** — custom hand-drawn icon at all sizes (16 → 256px)

---

## 📸 Preview

```
╔══════════════════════════════════════════╗
║ • lofi girl radio              ─    ✕   ║
╠══════════════════════════════════════════╣
║  [girl]  lofi girl radio                ║
║          00:00                          ║
║          vol ████░░░░ 80%               ║
║          ⏸  −  +                        ║
╠══════════════════════════════════════════╣
║ ● playing          made by corazonthedev ║
╚══════════════════════════════════════════╝
```

---

## 🚀 Quick Start

### Option A — Run from source

**1. Install dependencies**

```bash
pip install yt-dlp sounddevice numpy pillow pystray
```

**2. Install ffmpeg**

Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to your system `PATH`.  
Or place `ffmpeg.exe` in the same folder as `lofi_player.py`.

**3. Run**

```bash
python lofi_player.py
```

---

### Option B — Build .exe yourself

**1. Install PyInstaller**

```bash
pip install pyinstaller
```

**2. Build**

```bash
python -m PyInstaller --onefile --windowed --name "LofiGurl" --icon "LofiGurl.ico" lofi_player.py
```

**3. Find your executable**

```
dist/LofiGurl.exe
```

> ⚠️ `ffmpeg.exe` must be on your `PATH` or placed next to `LofiGurl.exe`.

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `yt-dlp` | Extracts the audio stream URL from YouTube |
| `sounddevice` | Low-latency audio output |
| `numpy` | PCM buffer manipulation & volume scaling |
| `pillow` | Generates the lofi girl `.ico` icon at runtime |
| `pystray` | System tray icon when minimized |
| `ffmpeg` *(external)* | Decodes and pipes audio to PCM |
| `tkinter` *(stdlib)* | GUI framework |

---

## 🗂️ Project Structure

```
LofiGurl/
├── lofi_player.py   # Main application
├── make_ico.py      # Standalone icon generator (outputs LofiGurl.ico)
├── LofiGurl.ico     # Pre-built icon (16–256px, multi-size)
├── requirements.txt # Python dependencies
└── README.md
```

---

## 🎮 Controls

| Action | How |
|---|---|
| Play / Pause | Click `⏸` / `▶` button |
| Volume Up | Click `+` button |
| Volume Down | Click `−` button |
| Set Volume | Click anywhere on the volume bar |
| Move window | Click and drag anywhere |
| Minimize to tray | Click `─` button |
| Restore from tray | Right-click tray icon → **Show** |
| Close | Click `✕` button or tray → **Quit** |

---

## 🔧 Configuration

At the top of `lofi_player.py` you can change:

```python
URL        = "https://www.youtube.com/watch?v=jfKfPfyJRdk"  # stream URL
SAMPLERATE = 44100   # audio sample rate
CHANNELS   = 2       # stereo
```

You can swap the URL for any other YouTube stream — 24/7 radios, jazz, classical, etc.

---

## ⚠️ Requirements

- **Windows 10 / 11** (uses `CREATE_NO_WINDOW` flag and Windows tray API)
- **Python 3.8+**
- **ffmpeg** on system `PATH`
- Active internet connection

---

## 📄 License

MIT © [corazonthedev](https://github.com/corazonthedev)

---

<div align="center">
  <sub>Built with ♥ and too many lofi playlists</sub>
</div>
