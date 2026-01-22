# Phase 3: Video Analysis

## Overview
Add video analysis capabilities including metadata display, snapshots, and recording.

## Tasks

- [ ] Display video metadata (FPS, resolution, codec)
- [ ] Snapshot capture
- [ ] Recording functionality

## Details

### 1. Video Metadata Display
- Extract and display:
  - Frame rate (FPS)
  - Resolution (width x height)
  - Codec information
  - Bitrate
  - Color space/format
  - Audio channels (if applicable)
- Real-time stats overlay option
- Metadata panel in sidebar

### 2. Snapshot Capture
- Capture current frame as image
- Save formats: PNG, JPEG
- Custom save location
- Auto-naming with timestamp
- Keyboard shortcut (e.g., F5)
- Batch snapshot (all cameras)

### 3. Recording Functionality
- Record individual camera streams
- Record all cameras simultaneously
- Output formats: MP4, AVI
- Configure recording quality
- Recording indicator in UI
- Auto-split by duration/size

## Data Model Extension

```sql
CREATE TABLE recordings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    camera_id INTEGER,
    file_path TEXT NOT NULL,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    file_size INTEGER,
    FOREIGN KEY (camera_id) REFERENCES cameras(id)
);

CREATE TABLE snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    camera_id INTEGER,
    file_path TEXT NOT NULL,
    captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (camera_id) REFERENCES cameras(id)
);
```

## UI Components

### Metadata Panel
```
+------------------------+
| Stream Info            |
+------------------------+
| Resolution: 1920x1080  |
| FPS: 30                |
| Codec: H.264           |
| Bitrate: 4000 kbps     |
| Color: YUV420P         |
+------------------------+
```

### Recording Controls
```
[Record] [Stop] [Snapshot]
Duration: 00:05:32
Size: 124.5 MB
```

## Acceptance Criteria
- [ ] Video metadata displays correctly
- [ ] Can capture snapshots from any camera
- [ ] Can record video streams
- [ ] Recordings are saved correctly
