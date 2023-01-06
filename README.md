# jed

This library aids with civis interactions.

## Tabler

* `tabler.get_table_names` returns a list of table names from Civis
* `tabler.get_related_table_names` returns a list of table names containing a
   specific topic.
* `tabler.get_table_id` returns the ID of a table in Civis given the schema and
   table name. The table_id is required for some other functions in Civis. 

# Jobber

* `jobber.list_job_chunk` returns a list of recent jobs. Civis uses a pagination
  system. This defaults to the latest 5 pages, but can return more by modifying the
  `pages` argument.
* `jobber.query_jobs_between` When given a DataFrame of jobs from
  `jobber.list_job_chunk`, returns jobs between `start_date` and `end_date`. This may
  not capture all dates if the original job didn't reach back far enough, so care should
  be taken.
