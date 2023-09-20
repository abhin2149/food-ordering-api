from odmantic import Model


# TODO Add validators
class User(Model):
    username: str
    password: str
    address: str


class UserResponse(Model):
    username: str
    address: str

