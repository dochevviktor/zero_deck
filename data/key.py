from command.command import Command
from command.command_type import CommandType
from util.image import render_key_image


class Key:
    def __init__(self, deck, page_number: int, button_number: int):
        self.deck = deck
        self.page_number = page_number
        self.button_number = button_number
        self.command = Command(CommandType.BLANK)
        self.image = None
        self.pressed_image = None

    def reload(self):
        with self.deck:
            self.deck.set_key_image(self.button_number, self.image)

    def press(self):
        with self.deck:
            self.deck.set_key_image(self.button_number, self.pressed_image)
            return self.command.run_command

    def load(self, key):
        self.command.command_type = CommandType.get_command(key.command.type)
        self.command.command = key.command.command
        self.image = render_key_image(self.deck, key, False)
        self.pressed_image = render_key_image(self.deck, key, True)
