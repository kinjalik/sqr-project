from pydantic.dataclasses import dataclass


@dataclass
class UserDataSchema:
    email: str
    hashed_password: str
