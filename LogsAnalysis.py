# "Database code" for the Logs Analysis Project.

import psycopg2

DBNAME = "news"

def popular_articles():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT * FROM top_paths;")
    test = c.fetchone()
    if not test:
        c.execute("CREATE VIEW top_paths AS "
                  "SELECT path, count(log.path) as num "
                  "FROM log "
                  "WHERE path LIKE '%article%' "
                  "GROUP BY path "
                  "ORDER BY num DESC "
                  "LIMIT 3;")
    c.execute("SELECT title, num "
              "FROM articles JOIN top_paths "
              "ON top_paths.path = '/article/' || articles.slug "
              "ORDER BY num DESC;")
    articles = c.fetchall()
    print articles
    db.close()

def popular_authors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT * FROM popular_authors;")
    test = c.fetchone()
    if not test:
        c.execute("CREATE VIEW popular_authors AS "
                  "SELECT author, count (log.path) AS views "
                  "FROM articles JOIN log "
                  "ON log.path = '/article/' || articles.slug "
                  "GROUP BY author "
                  "ORDER BY views DESC;")
    c.execute("SELECT * FROM popular_authors;")
    c.execute("SELECT authors.name, popular_authors.views "
              "FROM popular_authors JOIN authors "
              "ON authors.id = popular_authors.author "
              "ORDER BY popular_authors.viewS DESC;")
    authors = c.fetchall()
    print authors
    db.close()

def days_with_high_error_percentage():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # create a view that has dates and each date's statuses count
    # create view with dates and each date's 404 count
    # if count 404/count total status > .01: list day
    c.execute("SELECT * FROM dates_and_statuses;")
    test = c.fetchone()
    if not test:
        c.execute("CREATE VIEW dates_and_statuses AS "
                  "SELECT time::timestamp::date AS date, count (log.status) AS stat_count "
                  "FROM log "
                  "GROUP BY date;")
    c.execute("SELECT * FROM dates_and_404s;")
    test = c.fetchone()
    if not test:
        c.execute("CREATE VIEW dates_and_404s AS "
                  "SELECT time::timestamp::date AS date, count (log.status) AS errors "
                  "FROM log "
                  "WHERE status LIKE '%404%' "
                  "GROUP BY date;")
    c.execute("SELECT * FROM dates_and_percentages;")
    test = c.fetchone()
    if not test:
        c.execute("CREATE VIEW dates_and_percentages AS "
                  "SELECT dates_and_statuses.date, dates_and_404s.errors / dates_and_statuses.stat_count ::float AS percentage "
                  "FROM dates_and_404s JOIN dates_and_statuses "
                  "ON dates_and_404s.date = dates_and_statuses.date;")
    c.execute("SELECT * from dates_and_percentages;")
    d_and_s = c.fetchall()
    print d_and_s
    db.close()

if __name__ == '__main__':
    popular_articles()
    popular_authors()
    days_with_high_error_percentage()

# title1 = articles[0][0] #[[title, num]...] #print title1 <--first steps for formatting to plain text
