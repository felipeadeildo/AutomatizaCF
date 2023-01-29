from typing import Optional
from requests import Session
from abc import abstractmethod
from .base import Wrapper

class Whatsapp(Wrapper):
    def __init__(self, enviroment_vars: dict) -> None:
        self.session = self.create_session(enviroment_vars.get("WA_TOKEN_AUTH"))
        self.env_vars = enviroment_vars
    
    def __str__(self) -> str:
        return 'whatsapp'
    
    def create_session(self, auth_token: str) -> Session:
        """Create a Session for Wrapper

        Args:
            auth_token (str): Bearer Token

        Returns:
            requests.Session: Session of platform API
        """        
        session = Session()
        session.headers.update({
            "accept": "application/json",
            "authorization": f"Bearer {auth_token}",
            "user-agent": "CFSesh/v1" # Chef Special!
        })
        return session
    
    def send_message(self, user:str, message:str, preview_url: Optional[bool]=False) -> str:
        _payload = {
            "messaging_product": "whatsapp",
            "to": user,
            "type": "text",
            "text": {
                "body": message,
                "preview_url": preview_url
            }
        }
        response = self.session.post(self.env_vars.get("WA_API_MESSAGES"), json=_payload).json()
        if 'error' in response.keys():
            raise Exception(response['error'])
        return response['messages'][0]['id']