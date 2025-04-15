# Hand Tracking Mouse Control

A Python application that uses computer vision to control your mouse cursor with hand gestures. The application uses OpenCV and MediaPipe to track hand movements and allows you to control your computer's mouse cursor using natural hand gestures.

## Features

- Right hand controls cursor movement
- Left hand controls click and drag operations
- Real-time hand tracking visualization
- Smooth cursor movement
- Click and drag gestures

## Requirements

- Python 3.7+
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

## Installation

1. Clone this repository:

```bash
git clone https://github.com/AruneshwarAR/handTrackMouse.git
cd handTrackMouse
```

2. Create a virtual environment and install dependencies:

```bash
# Using UV
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Usage

1. Activate the virtual environment:

```bash
source .venv/bin/activate
```

2. Run the application:

```bash
python hand_track_mouse.py
```

3. Hand Gestures:

   - Right Hand: Move your index finger to control the cursor
   - Left Hand:
     - Quick pinch (thumb and index finger together briefly) to click
     - Hold pinch to drag
     - Release to stop dragging

4. Press 'q' to quit the application

## License

MIT License
