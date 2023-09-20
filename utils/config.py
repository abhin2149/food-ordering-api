from dotenv import dotenv_values


def get_config():
    return dotenv_values(".env")
