# Automated Home Security — Overview

A Python-based home security demo that uses facial recognition to identify known people from a live webcam feed.

## What it does

The system maintains a set of reference face images for known individuals. When "security mode" is activated, it captures video from a webcam, detects faces in each frame, and compares them against the stored encodings. Matched faces are highlighted with a bounding box on the live feed, which is displayed through a Streamlit web UI.

A Firebase Realtime Database integration exists to store structured metadata about known people (name, relationship, appearance details), with numeric IDs tying database records to reference images.

## Key capabilities

- **Live face detection and recognition** via webcam using `face_recognition` (dlib-based) and OpenCV
- **Streamlit UI** for toggling the live security feed on/off
- **Offline enrollment**: reference images in `verified_images/` are encoded and pickled for fast lookup
- **Firebase backend** (partially integrated) for persisting people metadata

## Tech stack

- Python 3
- Streamlit (UI)
- OpenCV + face_recognition + NumPy (vision/ML)
- Firebase Admin SDK (cloud database)

## Current state

The project is a functional prototype. The live recognition pipeline works end-to-end, but the Firebase integration is not yet wired into the real-time feed — people metadata is seeded separately and not surfaced in the UI. Several UI sections (Verified People, Config) are stubbed out but not implemented.
