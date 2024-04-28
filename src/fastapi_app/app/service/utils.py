import hashlib
import os
import secrets


def create_new_salt():
    return os.urandom(16)


def password_hash(password, s=None):
    if not s:
        s = create_new_salt()
    if not isinstance(s, bytes):
        s = bytes.fromhex(s)
    if not isinstance(password, bytes):
        password = password.encode("utf-8")

    pass_s = password + s
    return s.hex() + hashlib.sha256(pass_s).hexdigest()


def password_verification(password, passwd_hash):
    if not isinstance(password, bytes):
        password = password.encode("utf-8")
    check_hash = password_hash(password, passwd_hash[:32]).encode("utf-8")

    if not isinstance(passwd_hash, bytes):
        passwd_hash = passwd_hash.encode("utf-8")

    return secrets.compare_digest(check_hash, passwd_hash)
