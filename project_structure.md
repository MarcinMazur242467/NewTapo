# Project Structure: Classes and Methods

This document outlines the classes, methods, and key functions used in the project, organized by their core functionality.

### 1. Application Setup (`app/__init__.py`)

This file contains the core function to initialize and configure the Flask application.

*   **Function: `create_app()`**
    *   Initializes the Flask app, loads configuration, connects to the camera, starts video/audio streams, and registers web routes.

### 2. Camera Control (`app/camera/camera.py`)

This class manages the connection and control of the Tapo camera.

*   **Class: `TapoCamera`**
    *   `__init__(self, ip, user, password, cloudPassword)`: Initializes the camera with connection details.
    *   `connect(self)`: Establishes the RTSP video stream and administrative connection.
    *   `read_frame(self)`: Reads a single video frame from the camera's stream.
    *   `move(self, direction, step)`: Moves the camera's motor (pan/tilt).
    *   `release(self)`: Releases the video capture resource.

### 3. Streaming (`app/video/streamer.py` and `app/audio/streamer.py`)

These classes handle the continuous streaming of video and audio from the camera to the web client via WebSockets.

*   **Class: `VideoStreamer`**
    *   `__init__(self, camera, socketio)`: Initializes the streamer with the camera and SocketIO instances.
    *   `start_streaming(self)`: Starts the video capture and streaming thread.
    *   `_capture_loop(self)`: The main loop that reads frames, runs motion detection, and emits them.
*   **Class: `AudioStreamer`**
    *   `__init__(self, camera, socketio)`: Initializes the audio streamer.
    *   `start_streaming(self)`: Starts the audio capture and streaming thread.
    *   `_stream_loop(self)`: The main loop that reads audio packets, processes, and emits them.

### 4. Motion Detection (`app/detection/motion.py` and `app/detection/base.py`)

These classes are responsible for detecting motion in the video stream.

*   **Class: `BaseDetector` (Abstract)**
    *   `detect(self, frame)`: Defines the required interface for any detector class.
*   **Class: `MotionDetector`** (inherits from `BaseDetector`)
    *   `__init__(self, min_area)`: Initializes the detector with a minimum contour area to reduce false positives.
    *   `detect(self, frame)`: Compares the current frame to a running average to find differences indicating motion.

### 5. Recording (`app/recording/recorder.py`)

This class manages the recording of video and audio streams to a file.

*   **Class: `Recorder`**
    *   `__init__(self)`: Sets up the recorder and the save directory.
    *   `start_recording(self)`: Begins capturing frames and audio chunks into memory.
    *   `add_frame(self, frame)`: Adds a video frame to the current recording buffer.
    *   `add_audio(self, audio_data)`: Adds an audio chunk to the current recording buffer.
    *   `stop_recording(self)`: Stops recording and processes the buffered frames and audio, combining them into an `.mp4` file using `moviepy`.

### 6. Web Interface (Routes and Sockets)

These functions define the API endpoints and real-time WebSocket events for interacting with the application from the browser.

*   **Web Routes (`app/web/routes.py`)**
    *   `index()`: Renders the main camera control page.
    *   `move_camera()`: Handles POST requests to move the camera.
    *   `list_recordings()`: Renders the page listing all saved video files.
    *   `play_recording(filename)`: Streams a saved recording to the browser for playback.
    *   `download_recording(filename)`: Serves a recording file for download.
    *   `delete_recording(filename)`: Deletes a specified recording file.
*   **Socket Handlers (`app/web/socket_handlers.py`)**
    *   `handle_start_recording()`: Triggered by a client to start recording.
    *   `handle_stop_recording()`: Triggered by a client to stop recording.
    *   `handle_move_camera(data)`: Triggered by a client to control camera movement.

### 7. Configuration and Shared State

*   **`app/settings.py`**
    *   `load_config()`: Loads camera credentials and settings from `config.json`.
*   **`app/shared.py`**
    *   This module holds globally shared instances of the `TapoCamera`, `VideoStreamer`, `AudioStreamer`, and `Recorder` to make them accessible across different parts of the application.
