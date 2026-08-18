import argparse
from pathlib import Path

from .actuator import SortActuator
from .colors import load_color_ranges
from .detector import detect_colored_objects


def build_parser():
    p = argparse.ArgumentParser(description="OpenCV color object sorter")
    p.add_argument("--camera", type=int, default=0)
    p.add_argument("--port", help="Serial port for sorter actuator")
    p.add_argument("--baud", type=int, default=115200)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--config", default=str(Path(__file__).resolve().parents[2] / "config" / "colors.yaml"))
    p.add_argument("--min-area", type=float, default=900.0)
    p.add_argument("--gate-width", type=int, default=50, help="Trigger band width around frame center")
    return p


def run():
    args = build_parser().parse_args()
    import cv2

    serial_handle = None
    if not args.dry_run:
        if not args.port:
            raise SystemExit("--port is required unless --dry-run is used")
        import serial
        serial_handle = serial.Serial(args.port, args.baud, timeout=0.1)

    colors = load_color_ranges(args.config)
    actuator = SortActuator(serial_handle)
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise SystemExit(f"Could not open camera {args.camera}")

    stable_label = None
    stable_frames = 0

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            height, width = frame.shape[:2]
            gate_left = width // 2 - args.gate_width // 2
            gate_right = width // 2 + args.gate_width // 2
            cv2.rectangle(frame, (gate_left, 0), (gate_right, height), (255, 255, 255), 1)

            detections = detect_colored_objects(frame, colors, args.min_area)
            primary = detections[0] if detections else None

            if primary:
                x, y, w, h = primary.bbox
                cx, cy = primary.centroid
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                cv2.putText(frame, primary.label, (x, max(20, y - 8)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                if primary.label == stable_label:
                    stable_frames += 1
                else:
                    stable_label = primary.label
                    stable_frames = 1

                if gate_left <= cx <= gate_right and stable_frames >= 3:
                    actuator.sort(primary.label)
            else:
                stable_label = None
                stable_frames = 0

            cv2.imshow("CV Object Sorter", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        if serial_handle is not None:
            serial_handle.close()


if __name__ == "__main__":
    run()
