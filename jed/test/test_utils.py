from datetime import date

import numpy as np
from pytest import mark

from jed import utils


@mark.parametrize(
    "dt, expected",
    [
        (np.datetime64("2020-01-01"), np.datetime64("2020-01-01")),
        ("2020-01-02", np.datetime64("2020-01-02")),
        (date(2020, 1, 3), np.datetime64("2020-01-03")),
    ],
)
def test_format_date(dt, expected):
    """Should return expected date"""
    assert utils.format_date(dt) == expected


@mark.parametrize(
    "end, start, interval, expected",
    [
        ("2020-02-02", "2020-02-01", "D", 1),
        ("2020-02-02T22", "2020-02-02T21", "h", 1),
        ("2020-02-02T22", "2020-02-02T21", "m", 60),
        ("2020-02-02T22", "2020-02-02T21", "s", 60 * 60),
    ],
)
def test_date_diff(end, start, interval, expected):
    """Should return difference between two dates"""
    assert utils.date_diff(end, start, interval) == expected
