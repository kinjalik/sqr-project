from pydantic import BaseModel


class UserDataSchema(BaseModel):
    email: str
    hashed_password: str
