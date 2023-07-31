from app.database.schemas import DatabaseCredential

class DatabaseService:
    def build_credentials(self, credential_dict: dict) -> None:
        return DatabaseCredential(user_name=credential_dict['user_name'],
                                      password=credential_dict['password'],
                                      host_name=credential_dict['host_name'],
                                      database_name=credential_dict['database_name'],
                                      port=credential_dict['port'])

    