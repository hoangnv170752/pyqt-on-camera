# Phase 1: Basic Setup

## Overview
Set up the foundational project structure with PyQt6, VLC integration, and SQLite database.

## Tasks

- [x] Project structure
- [ ] PyQt6 main window with basic layout
- [ ] Single video widget with VLC integration
- [ ] SQLite database setup

## Details

### 1. Project Structure
Create the folder structure as defined in README.md with all necessary `__init__.py` files.

### 2. PyQt6 Main Window
- Create `src/app.py` with `MainWindow` class
- Set up basic menu bar (File, View, Help)
- Configure window size and title
- Add status bar for stream info

### 3. Single Video Widget
- Create `src/widgets/video_widget.py`
- Integrate python-vlc for video playback
- Support play, pause, stop controls
- Handle stream URL input

### 4. SQLite Database Setup
- Create `src/services/database.py`
- Initialize database with schema
- Implement CRUD operations for cameras
- Implement settings storage

## Dependencies
```
PyQt6>=6.5.0
python-vlc>=3.0.18
```

## Acceptance Criteria
- [ ] Application launches without errors
- [ ] Main window displays correctly
- [ ] Can play a single video stream
- [ ] Database file is created on first run
