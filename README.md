# Logs Analysis

This code pulls from the news database, which is a mock database for a fictional news site. This code will use three tables in the news database named articles, authors, and logs to answer the following questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Getting Started

This project requires Python 2.7, PostgreSQL 9.5.7, and the Python library psycopg2.

1. Download the newsdata sql database found here: https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip 
2. Extract the database to the directory containing LogsAnalysis.py
3. To build the reporting tool, load the site's data into your local database with the command ```psql -d news -f newsdata.sql```.
4. Run ```python LogsAnalysis.py```.

## Create Views

I chose to include the commands to create the necessary views in the .py file, so there is no need to recreate them. All the same, here they are for reference:

CREATE VIEW top_paths AS SELECT path, count(log.path) as num FROM log WHERE path LIKE '%article%' GROUP BY path ORDER BY num DESC LIMIT 3;

CREATE VIEW popular_authors AS SELECT author, count (log.path) AS views  FROM articles JOIN log  ON log.path = '/article/' || articles.slug GROUP BY author ORDER BY views DESC;

CREATE VIEW dates_and_statuses AS SELECT time::timestamp::date AS date, count (log.status) AS stat_count FROM log GROUP BY date;"

CREATE VIEW dates_and_404s AS SELECT time::timestamp::date AS date, count (log.status) AS errors FROM log WHERE status LIKE '%404%' GROUP BY date;

CREATE VIEW dates_and_percentages AS SELECT dates_and_statuses.date, dates_and_404s.errors / dates_and_statuses.stat_count ::float AS percentage FROM dates_and_404s JOIN dates_and_statuses ON dates_and_404s.date = dates_and_statuses.date;

## Author

Lilly Hartmetz

## Acknowledgments

https://stackoverflow.com/questions/14290857/sql-select-where-field-contains-words
https://discussions.udacity.com/t/project-logs-analysis/245190
https://stackoverflow.com/questions/6133107/extract-date-yyyy-mm-dd-from-a-timestamp-in-postgresql
https://stackoverflow.com/questions/28736227/postgresql-9-3-convert-to-float
https://gist.github.com/PurpleBooth/109311bb0361f32d87a2#file-readme-template-md
https://stackoverflow.com/questions/435424/postgresql-how-to-create-table-only-if-it-does-not-already-exist?noredirect=1&lq=1
https://stackoverflow.com/questions/8723574/in-postgres-can-you-set-the-default-formatting-for-a-timestamp-by-session-or-g
https://stackoverflow.com/questions/28142688/how-to-turn-input-number-into-a-percentage-in-python
https://stackoverflow.com/questions/21189346/shebang-line-for-python-2-7?lq=1
Trish Whetzel - Udacity 1:1 Appointments
