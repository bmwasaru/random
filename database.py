"""PostgreSQL and python using psycopg2"""

import logging
from os import environ

from psycopg2.extras import DictCursor
import psycopg2


class Database:
    def __init__(self, config):
        self.host = config.DATABASE_HOST
        self.username = config.DATABASE_USERNAME
        self.password = config.DATABASE_PASSWORD
        self.port = config.DATABASE_PORT
        self.dbname = config.DATABASE_NAME
        self.conn = None

    def connect(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    host=self.host,
                    username=self.username,
                    password=self.password,
                    dbname=self.dbname,
                    port=self.port
                )
            except psycopg2.DatabaseError as e:
                logging.error(e)
                raise e
            finally:
                logging.info('Database connection successfully')

    def select_rows(self, query):
        """Run a SQL Query to select rows from table"""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query)
            records = cur.fetchall()
        cur.close()

    def select_rows_dict_cursor(self, query):
        """Run SELECT query and return dictionaries."""
        self.connect()
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query)
            records = cur.fetchall()
        cur.close()
        return records

    def update_rows(self, query):
        """Run a SQL query to update rows in table."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()
            cur.close()
            return f"{cur.rowcount} rows affected."
