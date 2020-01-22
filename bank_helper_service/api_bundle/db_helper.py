from django.db import connection

# Db helper functions go here

class DB_helper:
    """ 
    To be used if multiple db's come up in the future.
    """
    def __init__(self, dbname, query):
        self.dbname = dbname
        self.get_branches_query = query

    def execute(self):
        # can be extended to get connection to different db if needed
        try:
            cursor = connection.cursor()
            cursor.execute(self.get_branches_query)
            colnames = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall() 
            response = []
            for row in rows:
                response.append(dict(zip(colnames, row)))
            return response
        except Exception as err:
            # TODO: Logger
            return []