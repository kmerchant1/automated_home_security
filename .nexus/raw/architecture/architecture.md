# Automated Home Security — Architecture

## Directory Structure

```
automated_home_security/
├── scripts/
│   ├── main.py                # Streamlit entry point
│   ├── security.py            # Live webcam recognition loop
│   ├── encoding_generator.py  # Offline face encoding pipeline
│   └── database.py            # Firebase seed script
├── resources/
│   ├── serviceAccountKey.json # Firebase service account credentials
│   └── verified_file.p        # Pickled face encodings + ID list
├── verified_images/
│   ├── 00001.png
│   ├── 00002.png
│   └── 00003.png
└── .gitignore
```

## Components

### `scripts/main.py` — UI Layer
The Streamlit app shell. Renders a sidebar with three navigation options (Live Feed, Verified People, Config). The Live Feed view exposes an "Activate Security" checkbox that triggers `run_security()`. The other two views are stubbed but not yet implemented. It also loads `verified_file.p` on startup, though the live loop re-derives encodings from disk independently.

### `scripts/security.py` — Recognition Engine
Contains `run_security()`, the core real-time loop:
1. Reads all images from `verified_images/` and builds an `id_list` from filenames.
2. Calls `generate_encodings()` to compute face embeddings for each reference image.
3. Opens the webcam (`cv2.VideoCapture(0)`) and processes frames in a loop.
4. Scales each frame to 25% for faster detection, then runs `face_recognition.face_locations` and `face_recognition.face_encodings`.
5. Compares detected encodings against the reference list using `compare_faces` and `face_distance`.
6. Draws a green bounding box on the best match and streams frames to the Streamlit UI via `st.empty().image()`.

### `scripts/encoding_generator.py` — Offline Enrollment
Standalone script for the enrollment phase:
- Loads images from `verified_images/`.
- Runs `face_recognition.face_encodings` on each (assumes exactly one face per image).
- Pickles `[encodings, id_list]` to `resources/verified_file.p` for later use.
- Also exports `generate_encodings()` as a reusable function (consumed by `security.py`).

### `scripts/database.py` — Firebase Seeder
One-time script that initializes Firebase Admin with the service account key and writes structured people records under the `People` node in the Realtime Database. Each record uses a numeric string key (`00001`, `00002`, `00003`) matching the image filenames. This script is not called by the main app at runtime.

## Data Flow

```
[verified_images/*.png]
        │
        ▼
encoding_generator.py  ──►  resources/verified_file.p
        │                           │
        │                     (loaded by main.py
        │                      on app startup)
        │
        ▼
security.py (re-encodes from disk each run)
        │
        ├── webcam frame → face_locations → face_encodings
        ├── compare_faces against reference encodings
        └── annotated frame → Streamlit UI


[database.py]  (run separately)
        │
        ▼
Firebase Realtime Database  ──  People/{id}: {name, relationship, ...}
(not yet connected to live pipeline)
```

## Architecture Patterns

- **Flat scripts layout**: no Python package structure; modules are siblings in `scripts/` and import each other directly.
- **Two-phase design**: offline enrollment (encoding generation) is decoupled from online recognition. Enrollment results are persisted as a pickle file.
- **ID-based linking**: filenames in `verified_images/` (e.g. `00001.png`) serve as primary keys that tie face encodings to Firebase people records — though the live pipeline does not yet resolve names from Firebase at match time.
- **Streamlit as runtime host**: the UI layer drives the recognition loop synchronously; the webcam loop runs inside the Streamlit process, blocking until the feed is stopped.

## Known Gaps

| Area | Issue |
|------|-------|
| Firebase integration | `database.py` uses a hard-coded absolute path for the service account key; not portable |
| Live pipeline | `run_security()` re-encodes images from disk on every activation instead of reusing `verified_file.p` |
| Name display | Recognized faces are not labeled with names from the database |
| Error handling | `generate_encodings` uses `face_encodings(img)[0]` with no guard for zero or multiple faces |
| UI completeness | "Verified People" and "Config" sidebar views are not implemented |
| Credentials | `serviceAccountKey.json` is committed to the repo and should be removed and rotated |
