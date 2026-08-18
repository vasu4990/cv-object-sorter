import argparse
import time

import cv2
import numpy as np
import serial

MIN_AREA = 1200
DEBOUNCE_SECONDS = 0.75

COLOR_RANGES = {
    "red": [((0, 100, 80), (10, 255, 255)), ((170, 100, 80), (180, 255, 255))],
    "green": [((35, 70, 60), (90, 255, 255))],
    "blue": [((90, 80, 60), (135, 255, 255))],
}

COMMANDS = {"red": "R", "green": "G", "blue": "B"}


def build_mask(hsv, ranges):
    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
    for low, high in ranges:
        mask |= cv2.inRange(hsv, np.array(low), np.array(high))
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask


def detect_objects(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    detections = []

    for color, ranges in COLOR_RANGES.items():
        mask = build_mask(hsv, ranges)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < MIN_AREA:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            moments = cv2.moments(contour)
            if moments["m00"] == 0:
                continue
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])
            detections.append({"color": color, "area": area, "bbox": (x, y, w, h), "center": (cx, cy)})

    return sorted(detections, key=lambda item: item["area"], reverse=True)


def main():
    parser = argparse.ArgumentParser(description="OpenCV color object sorter")
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--video", help="Optional video file instead of a camera")
    parser.add_argument("--port", help="Optional serial port, e.g. COM5 or /dev/ttyUSB0")
    parser.add_argument("--baud", type=int, default=115200)
    args = parser.parse_args()

    source = args.video if args.video else args.camera
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video source: {source}")

    link = serial.Serial(args.port, args.baud, timeout=0.1) if args.port else None
    if link:
        time.sleep(2.0)

    last_sent = {}

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            detections = detect_objects(frame)
            now = time.monotonic()

            for item in detections:
                color = item["color"]
                x, y, w, h = item["bbox"]
                cx, cy = item["center"]

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                cv2.circle(frame, (cx, cy), 4, (255, 255, 255), -1)
                cv2.putText(frame, f"{color} {int(item['area'])}", (x, max(20, y - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                if now - last_sent.get(color, 0.0) >= DEBOUNCE_SECONDS:
                    command = COMMANDS[color]
                    print(f"sort={color} command={command} center=({cx},{cy}) area={item['area']:.0f}")
                    if link:
                        link.write((command + "\n").encode("ascii"))
                    last_sent[color] = now

            cv2.imshow("CV Object Sorter", frame)
            if cv2.waitKey(1) & 0xFF in (27, ord("q")):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        if link:
            link.close()


if __name__ == "__main__":
    main()
