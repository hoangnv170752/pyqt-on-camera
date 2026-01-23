# Phase 2: Core Features

## Overview

Implement multi-camera viewing and stream management capabilities.

## Tasks

- [X] Multi-camera grid view (2x2, 3x3, 4x4)
- [X] Add/edit/delete camera sources
- [X] Stream URL management (RTSP, HTTP)
- [X] Local file playback

## Details

### 1. Multi-Camera Grid View

- Create `src/widgets/grid_view.py`
- Implement dynamic grid layouts (2x2, 3x3, 4x4)
- Allow switching between layouts via menu/toolbar
- Handle window resizing gracefully

### 2. Camera Source Management

- Create dialog for adding new cameras
- Edit existing camera configurations
- Delete cameras with confirmation
- Drag-and-drop to reorder cameras in grid

### 3. Stream URL Management

- Support RTSP streams: `rtsp://username:password@ip:port/path`
- Support HTTP streams: `http://ip:port/stream`
- Validate URLs before saving
- Store credentials securely

### 4. Local File Playback

- Open local video files (mp4, avi, mkv)
- File browser dialog
- Recent files list
- Drag-and-drop file support

## UI Components

```
+------------------------------------------+
|  File  View  Camera  Help                |
+------------------------------------------+
| +--------+ +--------+ +--------+ +------+|
| | Cam 1  | | Cam 2  | | Cam 3  | | Cam 4||
| |        | |        | |        | |      ||
| +--------+ +--------+ +--------+ +------+|
| +--------+ +--------+ +--------+ +------+|
| | Cam 5  | | Cam 6  | | Cam 7  | | Cam 8||
| |        | |        | |        | |      ||
| +--------+ +--------+ +--------+ +------+|
+------------------------------------------+
| Status: 8 cameras connected              |
+------------------------------------------+
```

## Acceptance Criteria

- [X] Can view multiple cameras simultaneously
- [X] Can add/edit/delete camera sources
- [X] Can switch between grid layouts
- [X] Can play local video files
