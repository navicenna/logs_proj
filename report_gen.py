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


if __name__=='__main__':
    conn = psycopg2.connect("dbname=news")
    write_article_report(conn, 'most_popular_articles.txt')

