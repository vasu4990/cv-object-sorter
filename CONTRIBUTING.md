# Contributing

- Keep color thresholds configurable rather than embedding lab-specific values in code.
- Add tests for classifier/protocol changes.
- Preserve dry-run behavior so the vision stack can be tested without moving hardware.
- Document lighting, camera, and mechanical conditions when adding measured performance claims.
- Run `pytest -q` and `python -m compileall -q src sorter.py` before submitting changes.
