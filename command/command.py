from typing import Callable

from StreamDeck.Devices.StreamDeck import StreamDeck
from command.command_type import CommandType
import command.system_command as sys_com
import command.serial_command as ser_com


class Command:
    def __init__(self, command_type: CommandType, command: str = ""):
        self.command_type = command_type
        self.command = command

    def run_command(self, deck: StreamDeck, change_page_fn: Callable[[int], None]):
        try:
            if self.command_type == CommandType.BLANK:
                pass
            elif self.command_type == CommandType.SYSTEM:
                sys_com.run_system_command(deck, self.command)
            elif self.command_type == CommandType.PAGE:
                sys_com.run_page_command(self.command, change_page_fn)
            elif self.command_type == CommandType.TEXT:
                ser_com.send_text_over_serial(self.command)
            elif self.command_type == CommandType.KEY_PRESS:
                ser_com.send_key_press_over_serial(self.command)
            else:
                print("Unknown command type {} with command {}".format(self.command_type, self.command))
        except Exception as e:
            print("Error while triggering command:", e)
            pass
