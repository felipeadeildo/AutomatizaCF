import dotenv
import MySQLdb
from os import system, name as os_name

clear_screen = lambda: system("cls" if os_name == "nt" else "clear")

class Initial:
    def __init__(self) -> None:
        clear_screen()
        print("Iniciando Conexão com o DB...")
        env_vars = dotenv.dotenv_values()
        self.conn = MySQLdb.connect(
            host=env_vars.get("DB_HOST"),
            port=int(env_vars.get("DB_PORT")),
            user=env_vars.get("DB_USER"),
            password=env_vars.get("DB_PASSWORD")
        )
        self.cur = self.conn.cursor()
        print("Conexão feita.")
        self.create_initial_schema(env_vars.get("DB_NAME"))
        self.create_initial_administrator(env_vars)
        print("Tarefas finalizadas com sucesso.")
    
    def create_initial_administrator(self, env_vars:dict):
        print("Criando administrador inicial...")
        self.conn.close()
        self.conn = MySQLdb.connect(
            host=env_vars.get("DB_HOST"),
            port=int(env_vars.get("DB_PORT")),
            user=env_vars.get("DB_USER"),
            password=env_vars.get("DB_PASSWORD"),
            database=env_vars.get("DB_NAME")
        )
        self.cur = self.conn.cursor()
        username = input("Insira username do administrador: ")
        role = input("Insira o nome do cargo do administrador: ")
        tg_user_id = input("Insira o ID da conta telegram desse administrador: ")
        password = input("Insira a senha desse amdinistrador: ")
        self.cur.execute("INSERT INTO workspace_users (username, role, tg_user_id, password, permission_level) VALUES (%s, %s, %s, %s, %s)", (username, role, tg_user_id, password, 100))
        self.conn.commit()
        self.conn.close()
        print("Administrador adicionado com sucesso!")
    
    def create_initial_schema(self, db_name:str):
        print("Criando schema inicial...")
        schema = {
            "general_users": [
                ("user_id", "text"),
                ("first_name", "text"),
                ("last_name", "text"),
                ("state", "text"),
                ("telefone", "text"),
                ("email", "text"),
                ("phone_number_id", "text"),
                ("platform", "text"),
            ],
            
            "relationed_messages": [
                ("from_user_id", "text"),
                ("platform", "text"),
                ("state", "text"),
                ("tg_msg_id", "text"),
            ],
            
            "setores": [
                ("setor_id", "int NOT NULL AUTO_INCREMENT PRIMARY KEY"),
                ("setor_name", "text"),
                ("setor_users", "text"),
                ("group_id", "text")
            ],
            
            "workspace_users": [
                ("username", "text"),
                ("role", "text"),
                ("permission_level", "int"),
                ("email", "text"),
                ("telefone", "text"),
                ("tg_user_id", "text"),
                ("password", "text"),
            ]
        }
        
        print(f"\tCriando DB com nome {db_name}...")
        try:
            self.cur.execute(f"CREATE DATABASE {db_name}") # por algum motivo, IF NOT EXISTS naõ estav funcionando...
            self.conn.commit()
        except:
            pass
        print(f"\tDB {db_name} criada.\n\tCriando tabelas...")
        self.cur.execute(f"USE {db_name}")
        for table_name, columns in schema.items():
            print(f"\t\tCriando a tabela {table_name}...")
            columns_type = ", ".join([' '.join(column) for column in columns])
            self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_type})")
            self.conn.commit()
            print(f"\t\tTabela {table_name} criada com sucesso!")

if __name__ == "__main__":
    Initial()