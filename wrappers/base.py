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
    
    @abstractmethod
    def send_file(self, user:str, file_url:str, file_type:str):
        """Envia um arquivo direto de uma URL

        Args:
            user (str): identificação do usuário
            file_url (str): url do arquivo
            file_type (str): "audio", "document", "image", "sticker" or "video".
        """
        pass
    
    @abstractmethod
    def mark_as_read(self, user:str, message_id:str):
        """Marca uma mensagem como lida

        Args:
            user (str): identificação do usuário
            message_id (str): id da mensagem
        """
        pass