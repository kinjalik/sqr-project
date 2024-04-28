import hashlib
import os
import secrets


def create_new_salt():
    return os.urandom(16)


def password_hash(self, password, s=None):
    if not s:
        s = create_new_salt()
    if not isinstance(password, bytes):
        password = password.encode("utf-8")
    pass_s = password + s
    return s.hex() + hashlib.sha256(pass_s).hexdigest()


def password_verification(self, password, password_hash):
    if not isinstance(password, bytes):
        password = password.encode("utf-8")
    check_hash = password_hash(password, password_hash[:16])
    return secrets.compare_digest(check_hash, password_hash)
