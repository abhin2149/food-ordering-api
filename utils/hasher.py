from passlib.hash import sha256_crypt


def hash_password(password):
    return sha256_crypt.hash(password)


def verify_password(encrypted_password, user_password):
    return sha256_crypt.verify(user_password, encrypted_password)
