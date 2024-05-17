from os import getenv
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import get_type_hints

load_dotenv(".env")

class AppConfigError(Exception):
    pass

def _parse_bool(val):
    return eval(val)

@dataclass
class AppConfig:
    ###### MYSQL Database Login Information ######
    MYSQL_USERNAME: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_DB_NAME: str
    MYSQL_TABLE_NAME: str

    ###### MYSQL Database Login Information ######
    PLAYER_1: str
    PLAYER_2: str

    def __init__(self):
        for field in self.__annotations__:
            default_value = getattr(self, field, None)

            if default_value is None and getenv(field) is None:
                raise AppConfigError('The {} field is required'.format(field))

            try:
                var_type = get_type_hints(AppConfig)[field]
                if var_type == bool:
                    value = _parse_bool(getenv(field, default_value))
                else:
                    value = var_type(getenv(field, default_value))
                self.__setattr__(field, value)

            except ValueError:
                raise AppConfigError(f'Unable to cast value of {getenv(field)} to type {var_type} for {field} field')

    def __repr__(self):
        return str(self.__dict__)

Config=AppConfig()
