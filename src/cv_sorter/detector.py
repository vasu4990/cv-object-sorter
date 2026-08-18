from dataclasses import dataclass

import cv2
import numpy as np

from .colors import HSVRange


@dataclass(frozen=True)
class Detection:
    label: str
    area: float
    centroid: tuple[int, int]
    bbox: tuple[int, int, int, int]


def mask_for_ranges(hsv_image, ranges: list[HSVRange]):
    mask = np.zeros(hsv_image.shape[:2], dtype=np.uint8)
    for candidate in ranges:
        lower = np.array(candidate.lower, dtype=np.uint8)
        upper = np.array(candidate.upper, dtype=np.uint8)
        mask = cv2.bitwise_or(mask, cv2.inRange(hsv_image, lower, upper))
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask


def detect_colored_objects(frame, color_ranges: dict[str, list[HSVRange]], min_area: float = 900.0) -> list[Detection]:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    detections: list[Detection] = []

    for label, ranges in color_ranges.items():
        mask = mask_for_ranges(hsv, ranges)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < min_area:
                continue
            moments = cv2.moments(contour)
            if moments["m00"] == 0:
                continue
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])
            detections.append(Detection(label, area, (cx, cy), cv2.boundingRect(contour)))

    return sorted(detections, key=lambda d: d.area, reverse=True)
