# "Database code" for the Logs Analysis Project.

import psycopg2

DBNAME = "news"

# It was recommended to me by a Udacity mentor in the live chat to use something like this to execute all of my queries,
#   but I haven't figured out how to utilize it:
# def execute_query(query):
#     db = psycopg2.connect(database=DBNAME)
#     c = db.cursor()
#     c.execute(query)
#     results = c.fetchall
#     db.close()
#     return results

def top_articles():
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
    print articles
    # c.execute("CREATE VIEW popular_authors AS "
    #           "SELECT author, count (log.path) AS views "
    #           "FROM articles JOIN log "
    #           "ON log.path = '/article/' || articles.slug "
    #           "GROUP BY author "
    #           "ORDER BY views desc;")
    db.close()  # when you close, it gets rid of your views

if __name__ == '__main__':
    top_articles()

# title1 = articles[0][0] #[[title, num]...] #print title1 <--first steps for formatting to plain text
