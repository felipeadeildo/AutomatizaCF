import telebot
from database.utils import load_db
from database.types import Setor, WorkspaceUser
from wrappers import wrappers_map

def leave_group(bot:telebot.TeleBot, message:telebot.types.Message):
    bot.leave_chat(message.chat.id)

class RelationedMessage:
    def __init__(self, from_user_id, platform, state, enviroment_vars) -> None:
        self.from_user_id = from_user_id
        self.platform = wrappers_map.get(platform)(enviroment_vars)
        self.state = state

class MessageHandler:
    def __init__(self, telegram_bot:telebot.TeleBot, message:telebot.types.Message, env_vars:dict) -> None:
        self.bot = telegram_bot
        self.message = message
        self.enviroment_vars = env_vars
        self.setor = None
        self.invoker = None
        self.relationed_message = None
        self.retrieve_message_info()
        if self.message.text.startswith("/"):
            self.args = self.message.text.split()
            self.command = self.args.pop(0)[1:]
            self.call_command()
    

    def retrieve_message_info(self):
        db_local = load_db(self.enviroment_vars["DB_PATH"])
        setor_info = db_local.execute("select  setor_id, setor_name, setor_users from setores where group_id = ?", (self.message.chat.id, )).fetchone()
        if setor_info is None and self.message.chat.type != 'private':
            return leave_group(self.message)
        if self.message.chat.type == 'private':
            setor_info = (self.message.chat.id, self.message.chat.username, self.message.chat.id.__str__())
        self.setor:Setor = Setor()
        self.setor._id, self.setor.name, self.setor.users = setor_info
        self.setor.users = self.setor.users.split()
        
        user_info = db_local.execute("select username, role, permission_level, email, telefone from workspace_users where tg_user_id = ?", (self.message.from_user.id, )).fetchone()
        if user_info is None:
            return #TODO: Adicioar um certo aviso aqui, não sei
        self.invoker:WorkspaceUser = WorkspaceUser()
        self.invoker.username, self.invoker.role, self.invoker.perm_level, self.invoker.email, self.invoker.telefone = user_info
        
        if self.message.reply_to_message is None:
            return
        relationed_message = db_local.execute("select from_user_id, platform, state from relationed_messages where tg_msg_id = ?", (self.message.reply_to_message.message_id, )).fetchone()
        if relationed_message is None:
            return
        self.relationed_message = RelationedMessage(relationed_message[0], relationed_message[1], relationed_message[2], self.enviroment_vars)

    def response_message(self):
        if self.relationed_message is None:
            return
        message_response = ' '.join(self.args)
        message_response = f"O {self.invoker.role} diz:\n\n{message_response}"
        self.relationed_message.platform.send_message(user=self.relationed_message.from_user_id, message=message_response)
        self.bot.reply_to(self.message, "Mensagem respondida com sucesso.")

    def call_command(self):
        if self.command == 'responder':
            self.response_message()

class CallbackHandler:
    def __init__(self) -> None:
        pass

class TelegramListener:
    def __init__(self, enviroment_vars:dict, telegram_bot: telebot.TeleBot) -> None:
        self.bot = telegram_bot 
        self.enviroment_vars = enviroment_vars
        self.start_handlers()
    
    def start_handlers(self):
        @self.bot.message_handler(func=lambda x: True)
        def call_handler_message(msg):
            MessageHandler(self.bot, msg, self.enviroment_vars)
        
        @self.bot.callback_query_handler(func=lambda x: True)
        def call_handler_callback(msg):
            CallbackHandler(self.bot, msg, self.enviroment_vars)
        
        self.bot.polling(non_stop=True)