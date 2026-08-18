# Computer Vision Object Sorter

An OpenCV-based object-sorting reference project that detects simple colored objects, classifies them, and emits actuator commands that can later drive a servo gate, conveyor diverter, or pick-and-place mechanism.

> **Status:** vision/software implementation. Camera calibration, lighting thresholds, conveyor timing, and actuator geometry must be tuned on the real machine.

## Features

- Live webcam or video-file input
- HSV color segmentation
- Morphological noise cleanup
- Contour filtering by area
- Centroid and bounding-box extraction
- Color classification for red, green, and blue objects
- Dry-run event output for testing without hardware
- Optional serial command output to a microcontroller

## Architecture

```text
Camera → HSV segmentation → contour filtering → object classifier
                                            ↓
                                     decision / debounce
                                            ↓
                                    serial actuator command
```

## Install

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python sorter.py --camera 0
```

To send decisions to a microcontroller:

```bash
python sorter.py --camera 0 --port COM5
```

## Default protocol

- `R` → red bin
- `G` → green bin
- `B` → blue bin

The physical controller should decide how to actuate the sorter safely; the vision process should not directly assume servo angles.

## Practical calibration

1. Lock camera exposure/white balance if possible.
2. Capture HSV values under the actual lighting.
3. Adjust ranges in `COLOR_RANGES`.
4. Tune `MIN_AREA` to reject background noise.
5. Measure the delay between camera detection and the actuator location.
6. Add an object tracker or encoder trigger if multiple objects can be in flight simultaneously.

## Future upgrades

- [x] Color segmentation and contour detection
- [x] Serial event output
- [x] Debounced detections
- [ ] Shape classifier
- [ ] Conveyor encoder synchronization
- [ ] Camera calibration / perspective correction
- [ ] YOLO-based general object detection
- [ ] Throughput and accuracy benchmark
- [ ] Demo video / confusion matrix
