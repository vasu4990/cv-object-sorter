# Computer Vision Object Sorter

[![Python CI](https://github.com/vasu4990/cv-object-sorter/actions/workflows/python.yml/badge.svg)](https://github.com/vasu4990/cv-object-sorter/actions/workflows/python.yml)

A modular OpenCV reference system for detecting colored objects on a conveyor/work surface and sending deterministic sort commands to a microcontroller-driven diverter.

> **Status:** vision/software reference complete; HSV thresholds, camera exposure, trigger region, conveyor timing, actuator angles, and mechanical delays require calibration on the actual sorter.

## Pipeline

```mermaid
flowchart LR
    C[Camera frame] --> H[BGR → HSV]
    H --> M[Configurable color masks]
    M --> F[Morphology / noise cleanup]
    F --> O[Contour + area filtering]
    O --> D[Centroid / bounding box]
    D --> G[Trigger gate + debounce]
    G --> P[Serial sort command]
    P --> A[Arduino actuator]
    A --> S[Physical sorting gate]
```

## Supported reference classes

- Red
- Green
- Blue
- Unknown/no detection

The ranges live in [`config/colors.yaml`](config/colors.yaml), not hard-coded into the detector.

## Install

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Run with webcam

Start in dry-run mode:

```bash
python sorter.py --dry-run
```

Use another camera index:

```bash
python sorter.py --camera 1 --dry-run
```

Connect a programmed actuator controller:

```bash
python sorter.py --port COM5
# Linux example: --port /dev/ttyACM0
```

Press `q` to quit.

## Serial protocol

The host sends newline-terminated single-character commands:

```text
R = red bin
G = green bin
B = blue bin
N = neutral/home
```

The included Arduino example controls a hobby servo diverter. Its angles are placeholders and **must** be calibrated to the real mechanism.

## Calibration

1. Lock camera position and exposure/white balance if possible.
2. Capture representative objects under real lighting.
3. Inspect HSV values and tune `config/colors.yaml`.
4. Tune minimum contour area to reject noise.
5. Set the on-screen trigger band so each object fires once.
6. Verify serial commands in dry-run/logging mode.
7. Calibrate diverter positions with the conveyor stopped.
8. Only then test moving objects at low conveyor speed.

See [`docs/CALIBRATION.md`](docs/CALIBRATION.md).

## Tests

```bash
pytest -q
```

Tests cover HSV range behavior, color classification, and command encoding.

## Repository layout

```text
.
├── src/cv_sorter/
│   ├── colors.py
│   ├── detector.py
│   ├── actuator.py
│   └── app.py
├── config/colors.yaml
├── firmware/sorter_actuator/sorter_actuator.ino
├── tests/
├── docs/
├── sorter.py
└── pyproject.toml
```

## Limitations

HSV thresholding is intentionally explainable and lightweight but can fail under strong illumination changes, reflections, shadows, or similar colors. A future version can replace the classifier with a trained detector while retaining the same trigger/actuator architecture.

## License

MIT — see [`LICENSE`](LICENSE).
