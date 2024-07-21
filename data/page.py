from typing import List

from data.key import Key
from StreamDeck.Devices.StreamDeck import StreamDeck


class Page:
    def __init__(self, number: int, deck: StreamDeck):
        self.number = number
        self.deck = deck
        self.key_count = deck.key_count()
        self.keys: List[Key] = [Key(deck, number, k) for k in range(self.key_count)]

    def reload(self):
        for key in self.keys:
            key.reload()
