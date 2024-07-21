from typing import Callable

from StreamDeck.Devices.StreamDeck import StreamDeck


brightness = 60


def run_page_command(command: str, change_page_fn: Callable[[int], None]):
    change_page_fn(int(command))


def run_system_command(deck: StreamDeck, command: str):
    global brightness
    if command == "exit":
        with deck:
            deck.set_brightness(60)
            deck.reset()
            deck.close()
    elif command == "brightness_up":
        with deck:
            brightness += 10 if brightness < 100 else 0
            deck.set_brightness(brightness)
    elif command == "brightness_down":
        with deck:
            brightness -= 10 if brightness > 0 else 0
            deck.set_brightness(brightness)
