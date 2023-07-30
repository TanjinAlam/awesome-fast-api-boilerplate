from pydantic import BaseModel


class DatabaseCredential(BaseModel):
    user_name : str
    password : str 
    host_name : str 
    database_name : str 
    port : str