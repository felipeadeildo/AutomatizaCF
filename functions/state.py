from database.types import GeneralUser
from sqlite3 import Connection
from wrappers.base import Wrapper
from wrappers import wrappers_map
from telebot import TeleBot

class StateProcess:
    def __init__(self, invoker:GeneralUser, messages_tree:dict, enviroment_vars:dict, loaded_db:Connection, wrapper:Wrapper, messages_info:dict, telegram_bot:TeleBot) -> None:
        self.tree = messages_tree
        self.env_vars = enviroment_vars
        self.invoker = invoker
        self.conn = loaded_db
        self.wrapper = wrapper(self.env_vars)
        self.messages_infos = messages_info
        self.telegram_bot = telegram_bot
        return self.process_state()
    
    def process_state(self):
        current_state = self.tree['state'][self.invoker.state]
        action = current_state.get('action')
        if action == 'send_message':
            message = current_state['params']["message"]
            preview_url = current_state["params"]["preview_url"]
            self.wrapper.send_message(user=self.invoker.user_id, message=message, preview_url=preview_url)
        elif action == 'forward_messages_to_telegram':
            chat_id = current_state['params']['chat_id']
            for message in self.messages_infos.get("messages", []):
                message = (
                    f"<b>Usuário:</b> {self.invoker.first_name}\n"
                    f"<b>Telefone:</b> {self.invoker.telefone}\n"
                    f"<b>ID:</b> {self.invoker.user_id}\n"
                    f"<b>Plataforma:</b> {self.invoker.platform}\n"
                    "\n<b>Diz o seguinte:</b>\n\n"
                    f"{message['text']['body']}"
                    )
                message_telegram = self.telegram_bot.send_message(chat_id, message, "HTML")
                self.conn.execute("insert into relationed_messages (from_user_id, platform, state, tg_msg_id) values (?, ?, ?, ?)", (self.invoker.user_id, self.invoker.platform, self.invoker.state, message_telegram.message_id))
                self.conn.commit()
        self.conn.execute("UPDATE general_users SET state = ?, first_name = ? WHERE user_id = ? AND platform = ?", (current_state.get('next_state'), self.invoker.first_name, self.invoker.user_id, self.invoker.platform))
        self.conn.commit()
        self.conn.close()