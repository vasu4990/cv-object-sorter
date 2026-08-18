# Hardware Integration

## Reference components

- USB/UVC webcam
- Host computer running Python/OpenCV
- Arduino-compatible microcontroller
- Hobby servo or another low-voltage diverter actuator
- Conveyor/work surface and bins

## Bring-up order

1. Run vision in `--dry-run` and tune detections.
2. Program the actuator controller and test `R`, `G`, `B`, `N` from a serial terminal with the conveyor stopped.
3. Calibrate servo angles so no commanded position stalls the mechanism.
4. Connect the host and confirm each class selects the intended bin.
5. Test one moving object at low speed.
6. Measure any camera-to-diverter delay needed for the actual geometry.

Keep hands clear of moving gates and conveyor mechanisms during automated operation.
