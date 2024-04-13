from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    pass


class DatabaseClient:
    def __init__(self, config: DatabaseConfig):
        pass
