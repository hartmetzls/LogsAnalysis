#!/usr/bin/env python2.7
# "Database code" for the Logs Analysis Project.

import psycopg2

DBNAME = "news"


def popular_articles():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("DROP VIEW IF EXISTS top_paths;")
    c.execute("CREATE VIEW top_paths AS "
              "SELECT path, count(*) as num "
              "FROM log "
              "GROUP BY path;")
    c.execute("SELECT title, num "
              "FROM articles JOIN top_paths "
              "ON top_paths.path = '/article/' || articles.slug "
              "ORDER BY num DESC "
              "LIMIT 3;")
    articles = c.fetchall()
    db.close()
    print ""
    print "What are the three most popular articles?\n"
    for title, views in articles:
        if views == 1:
            print '\t {} - {} view'.format(title, views)
        else:
            print '\t {} - {} views'.format(title, views)


def popular_authors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("DROP VIEW IF EXISTS popular_authors;")
    c.execute("CREATE VIEW popular_authors AS "
              "SELECT author, count (log.path) AS views "
              "FROM articles JOIN log "
              "ON log.path = '/article/' || articles.slug "
              "GROUP BY author "
              "ORDER BY views DESC;")
    c.execute("SELECT authors.name, popular_authors.views "
              "FROM popular_authors JOIN authors "
              "ON authors.id = popular_authors.author "
              "ORDER BY popular_authors.views DESC;")
    authors = c.fetchall()
    db.close()
    print ""
    print "Who are the most popular authors?\n"
    for author, views in authors:
        if views == 1:
            print '\t {} - {} view'.format(author, views)
        else:
            print '\t {} - {} views'.format(author, views)


def days_with_high_error_percentage():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("DROP VIEW IF EXISTS dates_and_statuses;")
    c.execute("CREATE VIEW dates_and_statuses AS "
              "SELECT time::date AS date, "
              "count (log.status) AS stat_count "
              "FROM log "
              "GROUP BY date;")
    c.execute("DROP VIEW IF EXISTS dates_and_404s;")
    c.execute("CREATE VIEW dates_and_404s AS "
              "SELECT time::date AS date, "
              "count (log.status) AS errors "
              "FROM log "
              "WHERE status LIKE '%404%' "
              "GROUP BY date;")
    c.execute("DROP VIEW IF EXISTS dates_and_percentages;")
    c.execute("CREATE VIEW dates_and_percentages AS "
              "SELECT dates_and_statuses.date, "
              "dates_and_404s.errors / dates_and_statuses.stat_count::float "
              "AS percentage "
              "FROM dates_and_404s JOIN dates_and_statuses "
              "ON dates_and_404s.date = dates_and_statuses.date;")
    c.execute("SELECT to_char(date, 'FMMonth FMDD YYYY'), "
              "percentage from dates_and_percentages WHERE percentage > .01;")
    dates = c.fetchall()
    db.close()
    print ""
    print "On what days did the error percentage rate exceed 1%?\n"
    for date, percentage in dates:
        print '\t{} - {:.1%}'.format(date, percentage)
    print ""


if __name__ == '__main__':
    popular_articles()
    popular_authors()
    days_with_high_error_percentage()
