# "Database code" for the Logs Analysis Project.

import psycopg2

DBNAME = "news"


def create_top_paths():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    # copy pastable format for debugging with psql console
    # CREATE VIEW top_paths AS SELECT path, count(log.path) as num FROM log WHERE path LIKE '%article%' GROUP BY path
    # ORDER BY num DESC LIMIT 3;
    c.execute("CREATE VIEW top_paths AS "
              "SELECT path, count(log.path) as num "
              "FROM log "
              "WHERE path LIKE '%article%' "
              "GROUP BY path "
              "ORDER BY num DESC "
              "LIMIT 3;")

    titles = c.execute("SELECT title, num "
                       "FROM articles JOIN top_paths "
                       "ON top_paths.path = '/article/' || articles.slug;")

    articles = c.fetchall()

    # title1 = articles[0][0] #[[title, num]...] #print title1 <--first steps for formatting to plain text

    db.close()  # when you close, it gets rid of your views
    return articles


def popular_articles():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    # copy pastable format for debugging with psql console
    # CREATE VIEW popular_articles AS SELECT author, count (log.path) AS views FROM articles JOIN log ON log.path =
    # '/article/' || articles.slug ORDER BY views desc;
    c.execute("CREATE VIEW popular_articles AS "
              "SELECT author, count (log.path) AS views "
              "FROM articles JOIN log "
              "ON log.path = '/article/' || articles.slug "
              "ORDER BY views desc;")

    pop_arts = c.fetchall
    return pop_arts


if __name__ == '__main__':
    print create_top_paths()
    print popular_articles()

