from enum import Enum


class CommandType(Enum):
    BLANK = 0
    SYSTEM = 1
    PAGE = 2
    TEXT = 3
    KEY_PRESS = 4

    @classmethod
    def get_command(cls, key: int):
        return cls(key)
