import pandas as pd
import sqlite3

def read_table_sqlite(conn,tbl)->pd.DataFrame:
    return pd.read_sql_query(f"SELECT * FROM {tbl}", conn)

def connect_database(db_path):
    return sqlite3.connect(db_path)

def close_database(conn):
    return conn.close()
      

