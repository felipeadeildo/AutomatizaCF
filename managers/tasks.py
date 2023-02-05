from database.utils import load_db
from time import sleep
from json import load as load_js
from wrappers import wrappers_map, Wrapper


class TaskListener:
    def __init__(self, enviroment_vars:dict) -> None:
        self.env_vars = enviroment_vars
        while True:
            sleep(float(self.env_vars.get("TASKS_DELAY")))
            self.conn = load_db(self.env_vars)
            columns = ['task_id', 'user_id', 'platform', 'message_type', 'first_name']
            try:
                tasks = self.conn.execute(f"SELECT {', '.join(columns)} FROM tasks WHERE done = 0").fetchall()
            except:
                continue
            tasks = [
                {key:value for key, value in zip(columns, task)} for task in tasks
            ]
            for task in tasks:
                self.execute_task(task)
            self.conn.close()
    
    def format_message(self, task:dict) -> str:
        message_raw, keys_to_format = self.get_message_format(task.get("message_type"))
        for key in keys_to_format:
            message_raw = message_raw.replace(f"|{key}|", task.get(key))
        return message_raw
    
    def send_message(self, task:dict):
        wrapper: Wrapper = wrappers_map.get(task.get("platform"))(self.env_vars)
        message = self.format_message(task)
        wrapper.send_message(user=task.get("user_id"), message=message, preview_url=self.preview_url)
    
    def execute_task(self, task:dict):
        action = task.get("action")
        if action == 'send_message':
            self.send_message(task)
        
        self.conn.execute("UPDATE tasks SET done = 1 WHERE task_id = %s", (task.get("task_id"), ))
        self.conn.commit()
    
    def get_message_format(self, message_type:str) -> list:
        messages_tree = load_js(open(self.env_vars.get("MESSAGES_TREE_PATH"), encoding="utf-8"))
        message_raw = messages_tree['message_format'][message_type]["content"]
        self.preview_url = messages_tree["message_format"][message_type]['preview_url']
        # TODO: Regex line to get keys bwtwen {} to format
        return (message_raw, []) # (messaga_raw, [key_to_formart])