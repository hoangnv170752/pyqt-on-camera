# PC CamTouch - A desktop app for multi-camera checking and comparing

A PyQt6 desktop application for streaming video, multi-camera viewing, and video analysis with local data storage.

---

## Features

- **Multi-camera screen viewing** - View multiple camera streams simultaneously in a grid layout
- **Video stream support** - RTSP, HTTP, and local file playback via VLC
- **Video analysis** - Get information like FPS, resolution, codec details
- **Local data storage** - SQLite database for storing camera configurations and settings
- **Easy integration** - Designed for ICC video management system compatibility

---

## Project Structure

```
pyqt-on-camera/
├── README.md
├── requirements.txt
├── main.py                 # Application entry point
├── docs/                   # Development documentation
│   ├── phase-1-basic-setup.md
│   ├── phase-2-core-features.md
│   ├── phase-3-video-analysis.md
│   └── phase-4-advanced-features.md
├── src/
│   ├── __init__.py
│   ├── app.py              # Main application window
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── video_widget.py # Single video player widget
│   │   └── grid_view.py    # Multi-camera grid layout
│   ├── services/
│   │   ├── __init__.py
│   │   ├── stream_manager.py   # Handle video streams
│   │   └── database.py         # SQLite database operations
│   └── models/
│       ├── __init__.py
│       └── camera.py       # Camera data model
├── data/
│   └── app.db              # SQLite database (auto-created)
└── config/
    └── settings.json       # User settings (auto-created)
```

---

## Tech Stack

| Component      | Technology         |
| -------------- | ------------------ |
| GUI Framework  | PyQt6              |
| Video Playback | python-vlc         |
| Database       | SQLite3 (built-in) |
| Configuration  | JSON               |

---

## Installation

### Prerequisites

- Python 3.10+
- VLC Media Player installed on your system

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd pyqt-on-camera

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

```bash
# Run the application
python main.py
```

---

## Development Plan

Version v0.0.1 - release

See detailed documentation in the [docs/](docs/) folder:

| Phase                                     | Description                                       | Status  |
| ----------------------------------------- | ------------------------------------------------- | ------- |
| [Phase 1](docs/phase-1-basic-setup.md)       | Basic Setup - PyQt6, VLC, SQLite                  | Done    |
| [Phase 2](docs/phase-2-core-features.md)     | Core Features - Multi-camera, Stream management   | Done    |
| [Phase 3](docs/phase-3-video-analysis.md)    | Video Analysis - Metadata, Snapshots, Recording   | Current |
| [Phase 4](docs/phase-4-advanced-features.md) | Advanced - SRGAN, ICC integration, Custom layouts | Pending |

---

## Configuration

Camera sources are stored in SQLite database with the following schema:

```sql
CREATE TABLE cameras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    type TEXT DEFAULT 'rtsp',  -- rtsp, http, file
    enabled INTEGER DEFAULT 1,
    position INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT
);
```

---

## What I Want

- Multi camera screen viewing, currently VLC gives only 1 view
- Open video recording to get information like FPS, color resolution, optical distortion
- Easy integration for ICC video management system
- Local storage for data

---

## Special Thanks

- [Psychic-CCTV](https://github.com/Fireboltz/Psychic-CCTV) - Inspiration for SRGAN image enhancement
- [VLC](https://github.com/videolan/vlc) - The backbone of video playback
