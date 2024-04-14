import psycopg
from psycopg.rows import dict_row


get_rates_query = """
select orig_code, dest_code, day, price from prices
where orig_code =  ANY(%(orig_code)s) AND dest_code = ANY(%(dest_code)s)
and %(date_from)s <= day and day <= %(date_to)s;
"""

# Fancy recursive query
# See https://www.postgresql.org/docs/current/queries-with.html#QUERIES-WITH-RECURSIVE
# Initally queries for regions with parent_slug %(region)s
# Repeatedly runs
# `SELECT r.slug FROM regions r INNER JOIN t ON r.parent_slug = t.slug'
# until there are no new changes
resolve_regions_query = """
WITH RECURSIVE t(slug) AS (
    SELECT slug FROM regions WHERE slug = %(region)s
    UNION
    SELECT r.slug FROM regions r INNER JOIN t ON r.parent_slug = t.slug
)

SELECT code FROM ports WHERE parent_slug in (SELECT t.slug FROM t)
"""


class rates_repository:
    # Used for error handling in case a connection needs to be closed
    __connected = False

    def __init__(self, conn_string):
        self.connection = psycopg.connect(conn_string, row_factory=dict_row)
        self.__connected = True

    def __del__(self):
        if self.__connected:
            self.connection.close()

    def get_rates(self, date_from, date_to, origin, destination):
        with self.connection.cursor() as cursor:
            cursor.execute(get_rates_query, {
                           'orig_code': origin,
                           'dest_code': destination,
                           'date_from': date_from,
                           'date_to': date_to,
                           })

            return cursor.fetchall()

    def resolve_regions(self, region):
        with self.connection.cursor() as cursor:
            cursor.execute(resolve_regions_query, {
                'region': region
            })
            return [item['code'] for item in cursor.fetchall()]
