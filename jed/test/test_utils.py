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
