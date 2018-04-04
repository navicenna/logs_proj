# This is a Python script used to generate some reports on the news database

import psycopg2


def fetch_results(conn, sql):
    """ Given a SQL connection and query, execute the query and return
        the results
    """
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    return results


def write_article_report(conn, outfile):
    """ Output a report detailing the top 3 most popular articles
    """
    sql_popular_articles = '''
    SELECT    title, access_count
    FROM      articles INNER JOIN 
              (SELECT path, count(*) AS access_count
              FROM log
              WHERE status = '200 OK'
              GROUP BY path) AS access ON
                    access.path LIKE '%'||articles.slug
    ORDER BY  access_count desc
    LIMIT     3
    '''
    results = fetch_results(conn, sql_popular_articles)
    with open(outfile, "w") as f:
        for item in results:
            f.write('"{}" -- {} views\n'.format(item[0], item[1]))


def write_author_report(conn, outfile):
    """ Output a report detailing the most popular authors
    """
    sql_popular_authors = '''
    SELECT    authors.name, sum(access_count) as views
    FROM      articles 
              INNER JOIN 
              (SELECT path, count(*) AS access_count
              FROM log
              WHERE status = '200 OK'
              GROUP BY path) AS access ON
                    access.path LIKE '%'||articles.slug
              INNER JOIN 
              authors on
                articles.author = authors.id
    GROUP BY  authors.name
    ORDER BY  views desc
    '''
    results = fetch_results(conn, sql_popular_authors)
    with open(outfile, "w") as f:
        for item in results:
            f.write('{} -- {} views\n'.format(item[0], item[1]))


def write_error_report(conn, outfile):
    """ Output a report detailing days in which there were a lot of errors
    """
    sql_errors = '''
    SELECT      CAST(time AS DATE) AS day, 
                ROUND(100 * 
                      SUM(CASE WHEN status='404 NOT FOUND' THEN 1 ELSE 0 END) / 
                      SUM(CASE WHEN status='200 OK' THEN 1 ELSE 0 END), 1) AS err
    FROM        log 
    GROUP BY    day 
    HAVING      ROUND(100 * 
                      SUM(CASE WHEN status='404 NOT FOUND' THEN 1 ELSE 0 END) / 
                      SUM(CASE WHEN status='200 OK' THEN 1 ELSE 0 END), 1) > 1
    ORDER BY    err DESC 
    ;
    '''
    results = fetch_results(conn, sql_errors)
    with open(outfile, "w") as f:
        for item in results:
            f.write('{:%B %d, %Y} -- {}% errors\n'.format(item[0], item[1]))


# Run the script -- connect to the PostgresSQL DB and output the three reports
if __name__ == '__main__':
    conn = psycopg2.connect("dbname=news")
    write_article_report(conn, 'most_popular_articles.txt')
    write_author_report(conn, 'most_popular_authors.txt')
    write_error_report(conn, 'errors.txt')
