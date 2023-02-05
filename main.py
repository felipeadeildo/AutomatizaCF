import dotenv
from threading import Thread
from telebot import TeleBot
from managers.tg import TelegramListener
from managers.api import APIListener
from managers.tasks import TaskListener

class Main:
    def __init__(self) -> None:
        self.enviroment = dotenv.dotenv_values()
        self.telegram_bot = TeleBot(self.enviroment.get("TG_TOKEN_BOT"))
        self.start_managers()
    
    def start_managers(self):
        thread = Thread(target=TelegramListener, args=(self.enviroment, self.telegram_bot))
        thread.start()
        
        thread = Thread(target=APIListener, args=(self.enviroment, self.telegram_bot))
        thread.start()
        
        thread = Thread(target=TaskListener, args=(self.enviroment, ))
        thread.start()

if __name__ == '__main__':
    Main()