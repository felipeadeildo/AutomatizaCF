from abc import abstractmethod
from typing import Optional

class Wrapper:
    @abstractmethod
    def __init__(self, enviroment_vars: dict) -> None:
        """Base class for wrappers (Beta)"""
    
    @abstractmethod
    def send_message(self, user:str, message:str, preview_url: Optional[bool] = False):
        """Envia uma mensagem para usuário especificado

        Args:
            user (str): identificação do usuário
            message (str): texto da emnsagem
            preview_url (Optional[bool]): Se haverá preview de url da primeira ocorrência de url na mensagem
        """
        pass