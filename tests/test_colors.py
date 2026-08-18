from cv_sorter.colors import HSVRange, classify_hsv


def test_range_contains():
    r = HSVRange((0, 100, 80), (10, 255, 255))
    assert r.contains((5, 150, 120))
    assert not r.contains((20, 150, 120))


def test_classification_with_split_red_ranges():
    ranges = {
        "red": [HSVRange((0, 100, 80), (10, 255, 255)), HSVRange((170, 100, 80), (179, 255, 255))],
        "green": [HSVRange((35, 70, 60), (85, 255, 255))],
    }
    assert classify_hsv((5, 200, 200), ranges) == "red"
    assert classify_hsv((175, 200, 200), ranges) == "red"
    assert classify_hsv((60, 200, 200), ranges) == "green"
    assert classify_hsv((100, 20, 20), ranges) is None
