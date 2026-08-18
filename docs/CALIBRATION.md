# Calibration Guide

## Camera and lighting

Mount the camera rigidly. Use consistent diffuse lighting and lock exposure/white balance if the camera allows it. Calibration performed under different lighting may not transfer.

## HSV thresholds

Capture representative objects, inspect their HSV values, and tighten the YAML ranges until the target remains detected while the background is rejected. Red normally needs two hue ranges because hue wraps near 0/179 in OpenCV HSV.

## Area threshold

Increase `--min-area` until small noise blobs disappear without rejecting real objects.

## Trigger band

The vertical center band is a simple event trigger. Adjust `--gate-width` and camera position so an object enters the band once before the physical diverter must act.

## Mechanical timing

If the actuator is downstream from the camera, a real conveyor may need travel-time compensation based on distance and belt speed. Measure this; do not guess it. The reference implementation intentionally fires at the camera gate and leaves downstream timing as a hardware integration step.
