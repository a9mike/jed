import pandas as pd
import numpy as np
from jed import jobs
from unittest.mock import Mock
import pytest


_DT1 = '2020-01-01'
_DT2 = '2020-01-03'
_LAST_RUN = {
    'id': 16,
    'startedAt': '2022-12-29T22:56:45.000Z',
    'finishedAt': '2022-12-30T03:27:02.000Z',
    'createdAt': '2022-12-27T03:27:02.000Z',
    'state': 'succeed'
}
_AUTHOR = {
    'id': 17,
    'name': 'Marlon James',
    'username': 'MJames',
    'initials': 'AM',
    'online': False
}
_NESTED_INFO = {'last_run': _LAST_RUN, 'author': _AUTHOR}
JOBS = [
    {'id': 'x', 'updated_at': _DT1, 'created_at': _DT1} | _NESTED_INFO,
    {'id': 'y', 'updated_at': _DT2, 'created_at': _DT2} | _NESTED_INFO,
]
JOBS_DF = (
    pd.DataFrame(JOBS)
    .astype({"updated_at": np.datetime64, "created_at": np.datetime64})
)


def test_list_job_chunk():
    """Should iterate five times and return a formatted DataFrame"""
    civis_client = Mock()
    civis_client.jobs.list.return_value = JOBS
    result = jobs.list_job_chunk(civis_client)

    expected_cols = [
        'id', 'updated_at', 'created_at', 'last_run',
        'author', 'started_at', 'finished_at',
        'author_id', 'author_name', 'author_username',
    ]

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 10
    assert list(result.columns) == expected_cols


def test_query_jobs_between():
    """Should only return data for _DT1"""
    result = jobs.query_jobs_between(JOBS_DF, _DT1, '2020-01-02')
    assert len(result) == 1


def test_query_jobs_between_error():
    """Should raise warning"""
    with pytest.raises(SyntaxWarning):
        jobs.query_jobs_between(JOBS_DF, _DT1, _DT1)


