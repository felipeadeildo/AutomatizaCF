import MySQLdb

class ResponseQuery:
    def __init__(self, cur) -> None:
        self.cur = cur
        self.fetchall = self.cur.fetchall
        self.fetchone = self.cur.fetchone
        self.fetchmany = self.cur.fetchmany


class MySQL:
    def __init__(self, enviroment_vars:dict) -> None:
        self.conn = MySQLdb.connect(
            host=enviroment_vars.get("DB_HOST"),
            port=int(enviroment_vars.get("DB_PORT")),
            user=enviroment_vars.get("DB_USER"),
            password=enviroment_vars.get("DB_PASSWORD"),
            database=enviroment_vars.get("DB_NAME")
        )
        self.cur = self.conn.cursor()
        self.commit = self.conn.commit
        self.close = self.conn.close
    
    def execute(self, query:str, variables:tuple = None):
        self.cur.execute(query=query, args=variables)
        return ResponseQuery(self.cur)

def load_db(enviroment_vars:dict):
    return MySQL(enviroment_vars)