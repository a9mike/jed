import numpy as np


def format_date(dt: np.datetime64 | str) -> np.datetime64:
    """Format datetime into np.datetime64 if not already"""
    if isinstance(dt, np.datetime64):
        return dt
    elif isinstance(dt, str):
        return np.datetime64(dt)
    else:
        try:
            return np.datetime64(str(dt))
        except TypeError:
            print("Check that dt is a string or datetime")
