from dotenv import dotenv_values


# get env properties
def get_config():
    return dotenv_values(".env")
