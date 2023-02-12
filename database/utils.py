import MySQLdb
import re

class ResponseQuery:
    def __init__(self, cur) -> None:
        self.cur = cur
        self.fetchall = self.cur.fetchall
        self.fetchone = self.cur.fetchone
        self.fetchmany = self.cur.fetchmany


class MySQL:
    def __init__(self, enviroment_vars:dict=None) -> None:
        if enviroment_vars is None:
            from dotenv import dotenv_values
            enviroment_vars = dotenv_values()
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

def sanitize_user_id(user_id:int|str, platform:str):
    if platform == 'whatsapp':
        user_id = re.sub(r'[-()\s.+]', "", user_id)
        # number_size = len(user_id)
        if user_id[3:5] == '99':
            user_id = user_id.replace("99", "9", 1)
        # if tam_number == 8:
        #     user_id = f"55829{user_id}"
        # elif tam_number == 9:
        #     user_id = f"5582{user_id}"
        # if number_size == 11:
        #     user_id = f"55{user_id}"
        # elif number_size == 13:
        #     user_id = user_id
        # else:
        #     user_id = None
    # TODO: Add elif platform == 'instagram';
    return user_id