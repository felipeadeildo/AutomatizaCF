import sqlite3

def load_db(db_path:str):
    return sqlite3.connect(db_path)