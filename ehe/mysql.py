import mysql.connector
import pandas as pd
import ehe


class MySql(object):
    def __init__(self):
        # set an mssql connection
        self._connection = None

    @property
    def connection(self):
        """mysql connection"""
        if self._connection is None or self._connection.database is None:
            # init a connection
            try:
                mydb = mysql.connector.connect(
                    timeout=2000,
                    autocommit=True,
                    **ehe.config['mysql'])
            #will try two times to connect
            except:
                mydb = mysql.connector.connect(
                    timeout=2000,
                    autocommit=True,
                    **ehe.config['mysql'])

        return self._connection

    @connection.setter
    def connection(self, value):
        self._connection = value

    @connection.deleter
    def connection(self):
        del self._connection
        self._connection = None

    def execute_update(self, query):
        """
        Execute the get/delete/insert/update query
        """
        with self.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)

    def execute_list(self, query):
        """return results as list"""
        return list(self.execute(query))


    def execute_to_dataframe(self, query):
        """
        Execute the query and return a pandas dataframe of the results
        """
        return pd.read_sql(query, self.connection)


    def insert_dataframe_to_table(self, table_name, insert_df,connection):
        with self.connection as connection:
            with connection.cursor() as cursor:
                pd.write_frame(insert_df, con=connection, name=table_name,flavor='mysql')

