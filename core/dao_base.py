import psycopg2
import config
from contextlib import contextmanager

class DAOBase:
    def __init__(self):
        self.conn = psycopg2.connect(**config.DB)
        self.cur = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        try:
            self.cur.close()
        except:
            pass
        try:
            self.conn.close()
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = psycopg2.connect(**config.DB)
    try:
        yield conn
    finally:
        conn.close()