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
    c.execute("SELECT title, num "
              "FROM articles JOIN top_paths "
              "ON top_paths.path = '/article/' || articles.slug;")
    articles = c.fetchall()
    # title1 = articles[0][0] #[[title, num]...] #print title1 <--first steps for formatting to plain text
    db.close()  # when you close, it gets rid of your views
    return articles

def popular_authors():
    print "cheese"
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    # copy pastable format for debugging with psql console
    c.execute("CREATE VIEW popular_authors AS "
              "SELECT author, count (log.path) AS views "
              "FROM articles JOIN log "
              "ON log.path = '/article/' || articles.slug "
              "GROUP BY author "
              "ORDER BY views desc;")
    c.execute("SELECT * FROM popular_authors;")
    pop_auths = c.fetchall
    db.close()
    return pop_auths


if __name__ == '__main__':
    print create_top_paths()
    print popular_authors()


