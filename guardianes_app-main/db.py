import sqlite3
from config import Config

def get_conn():
    conn = sqlite3.connect(Config.DB)
    conn.row_factory = sqlite3.Row
    return conn