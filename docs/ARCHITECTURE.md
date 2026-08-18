# Architecture

The sorter is split into four testable responsibilities:

1. **Color configuration** — HSV thresholds loaded from YAML.
2. **Detection** — image masking, morphology, contour filtering, centroids and bounding boxes.
3. **Trigger policy** — require a stable classification and centroid inside a gate band.
4. **Actuation** — encode a small serial command and enforce a cooldown.

This separation lets the camera pipeline run in `--dry-run` without attached machinery and makes it straightforward to replace HSV classification with a learned detector later.
