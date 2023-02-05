from flask import Flask, request
from database.utils import load_db
from functions.chat import ChatBot
from telebot import TeleBot

class APIListener:
    def __init__(self, enviroment_vars:dict, telegram_bot:TeleBot) -> None:
        self.app = Flask(__name__)
        self.env_vars = enviroment_vars
        self.telegram_bot = telegram_bot
        self.listen_api()
    
    def wa_subscribe(self, args_data):
        if args_data.get("hub.verify_token") != self.env_vars.get("WA_TOKEN_SUBSCRIBE"):
            return 'Permission Deinied'
        else:
            return args_data.get('hub.challenge')
    
    def listen_api(self):
        @self.app.route(self.env_vars.get("WA_API_ROUTE"), methods=['GET', 'POST'])
        def process_hook():
            args_data = request.args
            if args_data.get('hub.mode') == 'subscribe':
                return self.wa_subscribe(args_data)
            
            json_data = request.json
            if json_data is not None and json_data.get('entry'):
                for entry in json_data['entry']:
                    if entry.get('changes') is None:
                        continue
                    
                for change in entry['changes']:
                    if change['field'] == 'messages' and change.get('statuses') is None and change['value'].get("messages") is not None:
                        ChatBot(change['value'], platform='whatsapp', enviroment_vars=self.env_vars, telegram_bot=self.telegram_bot)
            return 'Ok.'
        
        # TODO: Adicionar listener para instagram e ademais.
        # TODO: Adicionar comentários do pq de alguns if's.
        self.app.run(self.env_vars.get("WEBHOOK_HOST"), self.env_vars.get("WEBHOOK_PORT"))