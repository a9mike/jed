import civis
import numpy as np
import pandas as pd

from jed import utils


def list_job_chunk(civis_client: civis.APIClient, pages: int = 5) -> pd.DataFrame:
    """
    Returns a DataFrame of recently run civis jobs.

    jobs.list either returns 50 or less jobs (limit argument only lets you return less
    than 50 jobs) or you can iterate through ALL jobs (iterator=True) which takes a
    long time and returns everything from all time. You can also request specific pages
    but need to know what information your page is on (which will change with every
    new job run). This gives us more data returned and iterates through pages, so we
    don't have to do it each time. It's still a bit hacky but better than what civis
    has on offer.

    :param civis_client:
        CIVIS client generated with given API key or environment key.
    :param pages:
        Number of pages to grab. There are 50 jobs per page, most recent pages
        are first.
    """
    jobs = []
    for page in range(pages):
        corrected_page = page + 1  # correct for python indexing
        jobs = jobs + civis_client.jobs.list(page_num=corrected_page)

    return _jobs_to_df(jobs)


def _jobs_to_df(jobs: list) -> pd.DataFrame:
    """
    Formats job list into a DataFrame. Unpacks last_run and author columns so data can
    be accessed unnested in DataFrame. If there are duplicate columns in last_run,
    author, and base dataframe, it takes the base column. Formats date columns as dates.
    :param jobs:
        list of jobs from civis
    :return:
        Formatted DataFrame of jobs
    """
    unpacked_jobs = []
    for job in jobs:
        df = pd.DataFrame([job])
        # tried to operate listwise but sometimes we get
        last_run = pd.DataFrame([job["last_run"]])
        author = pd.DataFrame([job["author"]])
        # if last_run or author are empty
        last_run_empty = len(job["last_run"]) == 0
        if last_run_empty:
            last_run_cols = [
                "id",
                "state",
                "createdAt",
                "startedAt",
                "finishedAt",
                "error",
            ]
            last_run = pd.DataFrame({}, columns=last_run_cols)
        author_empty = len(job["author"]) == 0
        if author_empty:
            author_cols = ["id", "name", "username", "initials", "online"]
            author = pd.DataFrame({}, columns=author_cols)
        # update cols and col names
        for col in ["online", "initials"]:  # TODO: functionize this
            if col in author.columns:
                author = author.drop(columns=[col])
        author.columns = [f"author_{col}" for col in author.columns]
        for col in ["state", "createdAt", "id"]:  # TODO: functionize this
            if col in last_run.columns:
                last_run = last_run.drop(columns=[col])

        unpacked_jobs = unpacked_jobs + [pd.concat([df, last_run, author], axis=1)]

    date_cols = ["updated", "created", "started", "finished"]
    date_col_mapping = {f"{col}_at": np.datetime64 for col in date_cols}
    return (
        pd.concat(unpacked_jobs, axis=0)
        .rename(columns={"startedAt": "started_at", "finishedAt": "finished_at"})
        .astype(date_col_mapping)
    )


def query_jobs_between(
    jobs_df: pd.DataFrame,
    start_date: np.datetime64 | str,
    end_date: np.datetime64 | str,
) -> pd.DataFrame:
    """
    Return jobs that were updated between start_date and end_date, inclusive, from
    given dataframe.
    # TODO: check whether max/min dates are outside of start_date/end_date otherwise
    #  might need to pull more data
    #  TODO: combine filter_jobs_between and list_job_chunk into one job
    #   `list_jobs_between`
    """
    start = utils.format_date(start_date)
    end = utils.format_date(end_date)
    if start == end:
        raise SyntaxWarning("Start and end date should not be identical.")
    return jobs_df.query("(@start <= updated_at)").query("updated_at <= @end")
