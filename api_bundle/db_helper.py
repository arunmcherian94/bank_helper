from django.db import connection

# Db helper functions go here

class DB_helper:
    """ 
    To be used if multiple db's come up in the future.
    """
    def __init__(self, dbname, query, replacements = None):
        self.dbname = dbname
        self.get_branches_query = query
        self.query_replacements = replacements

    def execute(self):
        # can be extended to get connection to different db if needed
        try:
            cursor = connection.cursor()
            cursor.execute(self.get_branches_query, self.query_replacements)
            colnames = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall() 
            response = []
            for row in rows:
                response.append(dict(zip(colnames, row)))
            return response
        except Exception as err:
            # TODO: Logger
            return []