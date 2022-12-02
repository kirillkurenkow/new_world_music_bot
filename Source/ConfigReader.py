from configparser import (
    ConfigParser,
    NoSectionError,
    NoOptionError,
)
from os import path
from typing import (
    Any,
    Union,
)

__all__ = ['ConfigReader']


class ConfigReader(ConfigParser):
    def __init__(self, filename: str, config_encoding: str = 'utf-8'):
        """
        :param filename: Config filename
        :param config_encoding: Config encoding
        """
        super().__init__()
        self.__filename = filename
        self.__read_config(encoding=config_encoding)

    def __read_config(self, encoding: str = 'utf-8') -> None:
        """
        Read config
        """
        if not path.exists(self.__filename):
            raise FileNotFoundError(f'Не найден файл конфигурации: {self.__filename}')
        self.read(self.__filename, encoding=encoding)

    def get(self, section: str, option: str, *args, to_type: type = None, **kwargs, ) -> Any:
        """
        Get value from a section

        :param section: Section
        :param option: Option
        :param to_type: The type to convert the value to

        :return: to_type(value)
        """
        try:
            result = super().get(section=section, option=option, *args, **kwargs)
        except NoSectionError:
            raise
        except NoOptionError:
            raise
        if to_type is not None:
            try:
                result = to_type(result)
            except ValueError:
                raise ValueError(
                    f'Value "{option}" in section "{section}" can`t be converted to type "{to_type}"')
        return result

    def getint(self, section: str, option: str, *args, **kwargs, ) -> int:
        """
        Get int value from a section

        :param section: Section
        :param option: Option

        :return: int(Option)
        """
        return self.get(section, option, *args, to_type=int, **kwargs)

    def getfloat(self, section: str, option: str, *args, **kwargs, ) -> float:
        """
        Get float value from a section

        :param section: Section
        :param option: Option

        :return: float(Option)
        """
        return self.get(section, option, *args, to_type=float, **kwargs)

    def getnumber(self, section: str, option: str, *args, **kwargs) -> Union[int, float]:
        """
        Get int or float value (depending on the received value) from a section

        :param section: Section
        :param option: Option

        :return: [int|float](Option)
        """
        result = self.getfloat(section, option, *args, **kwargs)
        result = int(result) if result.is_integer() else result
        return result
