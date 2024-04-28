import pytest
from app.service.utils import password_hash, password_verification


@pytest.mark.parametrize(
    ("email", "password"), [("test1@mail.ru", "1234"), ("test2@mail.ru", "4321")]
)
def test_password_hashing(email, password):
    hash = password_hash(str(password))
    assert password_verification(password, hash)
