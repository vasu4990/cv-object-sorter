from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class HSVRange:
    lower: tuple[int, int, int]
    upper: tuple[int, int, int]

    def contains(self, hsv: tuple[int, int, int]) -> bool:
        return all(lo <= value <= hi for value, lo, hi in zip(hsv, self.lower, self.upper))


def load_color_ranges(path: str | Path) -> dict[str, list[HSVRange]]:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    result: dict[str, list[HSVRange]] = {}
    for name, ranges in raw["colors"].items():
        result[name] = [HSVRange(tuple(item["lower"]), tuple(item["upper"])) for item in ranges]
    return result


def classify_hsv(hsv: tuple[int, int, int], ranges: dict[str, list[HSVRange]]) -> str | None:
    for label, candidates in ranges.items():
        if any(candidate.contains(hsv) for candidate in candidates):
            return label
    return None
