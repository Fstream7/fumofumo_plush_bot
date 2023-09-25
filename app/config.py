import yaml
from os import path
from typing import get_type_hints, Union


class AppConfigError(Exception):
    pass


def _parse_bool(val: Union[str, bool]) -> bool:
    return val if type(val) is bool else val.lower() in ["true", "yes", "1"]


# AppConfig class with required fields, default values, type checking, and typecasting for int and bool values
class AppConfig:
    TOKEN: str
    LOG_LEVEL: str = "INFO"
    ADMIN_LISTS: list
    THANKS_STIKERS: list

    def __init__(self, env):
        for field in self.__annotations__:
            if not field.isupper():
                continue

            # Raise AppConfigError if required field not supplied
            default_value = getattr(self, field, None)
            if default_value is None and env.get(field) is None:
                raise AppConfigError("The {} field is required".format(field))

            # Cast env var value to expected type and raise AppConfigError on failure
            try:
                var_type = get_type_hints(AppConfig)[field]
                if var_type == bool:
                    value = _parse_bool(env.get(field, default_value))
                else:
                    value = var_type(env.get(field, default_value))

                self.__setattr__(field, value)
            except ValueError:
                raise AppConfigError(
                    'Unable to cast value of "{}" to type "{}" for "{}" field'.format(
                        env[field], var_type, field
                    )
                )

    def __repr__(self):
        return str(self.__dict__)


# Expose Config object for app to import
BASE_DIR = path.abspath(path.dirname(__file__))
with open(path.join(BASE_DIR, "config.yml"), encoding='utf-8') as file:
    Config = AppConfig(yaml.safe_load(file))
