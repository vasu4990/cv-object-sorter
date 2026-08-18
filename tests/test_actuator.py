import pytest

from cv_sorter.actuator import encode_sort_command


def test_command_encoding():
    assert encode_sort_command("red") == b"R\n"
    assert encode_sort_command("green") == b"G\n"
    assert encode_sort_command("blue") == b"B\n"


def test_unknown_label():
    with pytest.raises(ValueError):
        encode_sort_command("orange")
