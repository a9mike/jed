import civis
import numpy as np


def get_client(civis_client: civis.APIClient | None = None) -> civis.APIClient:
    """Check for civis client, if none generate one"""
    client = civis_client
    if not civis_client:
        client = civis.APIClient()
    return client


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


def date_diff(
    end: np.datetime64 | str,
    start: np.datetime64 | str,
    interval: str = "m",
) -> int | float:
    """
    Get difference between two dates.
    :param end:
        End time
    :param start:
        Start time
    :param interval:
        'D', 'h', 's', 'm'
    """
    return (format_date(end) - format_date(start)).astype(f"timedelta64[{interval}]")
