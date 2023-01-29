class Setor:
    _id:int|str = None
    name:str = None
    users:str|list = None

class WorkspaceUser:
    username:str = None
    role:int|str = None
    perm_level:int = None
    email:str = None
    telefone:str = None

class GeneralUser:
    first_name:str = None
    last_name:str = None
    user_id:str|int = None
    platform:str = None
    state:str = None
    telefone:str = None
    email:str = None
    phone_number_id:int|str = None
    