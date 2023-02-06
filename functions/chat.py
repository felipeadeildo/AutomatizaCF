from database.utils import load_db, sanitize_user_id
from database.types import GeneralUser
from wrappers import wrappers_map, Wrapper
from json import load as load_jsonfile
from functions.state import StateProcess
from telebot import TeleBot
import openai

class ChatBot:
    def __init__(self, messages_infos:dict, platform:str, enviroment_vars:dict, telegram_bot:TeleBot) -> None:
        self.env_vars = enviroment_vars
        self.messages_infos = messages_infos
        self.platform = wrappers_map.get(platform)
        self.retrieve_invoker(platform)
        self.platform(self.env_vars).mark_as_read(self.invoker.user_id, self.messages_infos["messages"][0]["id"])
        self.messages_tree = load_jsonfile(open(self.env_vars.get("MESSAGES_TREE_PATH"), "r", encoding="utf-8"))
        self.telegram_bot = telegram_bot
        if self.messages_infos['messages'][0]['text']['body'].startswith(self.env_vars.get("COMMAND_PREFIX")):
            self.execute_command()
        else:
            self.execute_state()

    def retrieve_invoker(self, platform:str):
        self.invoker = GeneralUser()
        self.invoker.user_id = sanitize_user_id(self.messages_infos['messages'][0]['from'])
        self.invoker.phone_number_id = self.messages_infos['metadata']['phone_number_id']
        
        conn = load_db(self.env_vars)
        invoker_infos = conn.execute("SELECT first_name, last_name, state, telefone, email FROM general_users WHERE (user_id = %s OR phone_number_id = %s) AND platform = %s", (self.invoker.user_id, self.invoker.phone_number_id, platform)).fetchone()
        if invoker_infos:
            self.invoker.first_name, self.invoker.last_name, self.invoker.state, self.invoker.telefone, self.invoker.email = invoker_infos
            self.invoker.first_name = self.invoker.first_name if self.invoker.first_name == self.messages_infos.get("contacts", [{"profile": {'name': ''}}])[0].get("profile")['name'] else self.messages_infos['contacts'][0]["profile"]['name']
        else:
            user_name = self.messages_infos["contacts"][0]['profile']['name'] if self.messages_infos.get("contacts") is not None else "Usuário"
            conn.execute("insert into general_users (first_name, last_name, state, telefone, user_id, phone_number_id, platform) values (%s, %s, %s, %s, %s, %s, %s)", (user_name, '-', 'init', self.invoker.user_id, self.invoker.user_id, self.invoker.phone_number_id, platform))
            conn.commit()
            conn.close()
            return self.retrieve_invoker(platform)
        self.invoker.platform = platform
        conn.execute("update general_users set first_name = %s where (user_id = %s or phone_number_id = %s) and platform = %s", (self.invoker.first_name, self.invoker.user_id, self.invoker.phone_number_id, self.invoker.platform))
        conn.commit()
        conn.close()
    
    def execute_state(self):
        state_obj = StateProcess(self.invoker, self.messages_tree, self.env_vars, load_db(self.env_vars), self.platform, self.messages_infos, self.telegram_bot)
    
    def ask_chatgpt(self):
        openai.api_key = self.env_vars.get("OPENAI_API_KEY")
        prompt = " ".join(self.args)
        completion = openai.Completion.create(engine="text-davinci-003", prompt=prompt, temperature=0.9, max_tokens=4000, n=1, stop=None)
        self.platform = self.platform(self.env_vars)
        self.platform.send_message(self.invoker.user_id, completion.choices[0].text)
    
    def askimg_chatgpt(self):
        openai.api_key = self.env_vars.get("OPENAI_API_KEY")
        if 'x' in self.args[0]:
            size = self.args.pop(0)
        else:
            size = '1024x1024'
        prompt = " ".join(self.args)
        try:
            image = openai.Image.create(prompt=prompt, n=1, size=size)
        except:
            pass
        else:
            self.platform = self.platform(self.env_vars)
            self.platform.send_file(self.invoker.user_id, image["data"][0]["url"], "image")
    
    def command_doesnt_exists(self):
        messages_tree = load_jsonfile(open(self.env_vars.get("MESSAGES_TREE_PATH"), encoding="utf-8"))
        message_text = messages_tree["message_format"]["command_doesnt_exists"]["content"]
        message_text = message_text.replace("|command|", self.command)
        self.platform(self.env_vars).send_message(self.invoker.user_id, message_text)

    def return_rotina(self):
        messages_tree = load_jsonfile(open(self.env_vars.get("MESSAGES_TREE_PATH"), encoding="utf-8"))
        message_text = messages_tree["message_format"]["rotina"]["content"]
        self.platform(self.env_vars).send_message(self.invoker.user_id, message_text)

    def execute_command(self):
        self.args = self.messages_infos['messages'][0]['text']['body'].split()
        self.command = self.args.pop(0)[len(self.env_vars.get("COMMAND_PREFIX")):]
        if self.command == 'ask':
            self.ask_chatgpt()
        elif self.command == 'askimg':
            self.askimg_chatgpt()
        elif self.command == 'rotina':
            self.return_rotina()
        else:
            self.command_doesnt_exists()