LogsAnalysis

This code pulls from the news database tables articles, authors, and logs to answer the following questions:
What are the most popular three articles of all time?
Who are the most popular article authors of all time?
On which days did more than 1% of requests lead to errors?

Getting Started

This code operates on python, a virtual machine such as vagrant, and postgreSQL.

What things you need to install the software and how to install them:

https://classroom.udacity.com/nanodegrees/nd000/parts/b910112d-b5c0-4bfe-adca-6425b137ed12/modules/a3a0987f-fc76-4d14-a759-b2652d06ab2b/lessons/0aa64f0e-30be-455e-a30d-4cae963f75ea/concepts/a9cf98c8-0325-4c68-b972-58d5957f1a91

Create Views

I chose to include the commands to create the necessary views in the .py file, so there is no need to recreate them. All the same, here they are for reference:

CREATE VIEW top_paths AS SELECT path, count(log.path) as num FROM log WHERE path LIKE '%article%' GROUP BY path ORDER BY num DESC LIMIT 3;

CREATE VIEW popular_authors AS SELECT author, count (log.path) AS views  FROM articles JOIN log  ON log.path = '/article/' || articles.slug GROUP BY author ORDER BY views DESC;

CREATE VIEW dates_and_statuses AS SELECT time::timestamp::date AS date, count (log.status) AS stat_count FROM log GROUP BY date;"

CREATE VIEW dates_and_404s AS SELECT time::timestamp::date AS date, count (log.status) AS errors FROM log WHERE status LIKE '%404%' GROUP BY date;

CREATE VIEW dates_and_percentages AS SELECT dates_and_statuses.date, dates_and_404s.errors / dates_and_statuses.stat_count ::float AS percentage FROM dates_and_404s JOIN dates_and_statuses ON dates_and_404s.date = dates_and_statuses.date;

Author

Lilly Hartmetz

Acknowledgments

https://stackoverflow.com/questions/14290857/sql-select-where-field-contains-words
https://discussions.udacity.com/t/project-logs-analysis/245190
https://stackoverflow.com/questions/6133107/extract-date-yyyy-mm-dd-from-a-timestamp-in-postgresql
https://stackoverflow.com/questions/28736227/postgresql-9-3-convert-to-float
https://gist.github.com/PurpleBooth/109311bb0361f32d87a2#file-readme-template-md
https://stackoverflow.com/questions/435424/postgresql-how-to-create-table-only-if-it-does-not-already-exist?noredirect=1&lq=1
Trish Whetzel - Udacity 1:1 Appointments
