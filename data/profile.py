from typing import List, Callable

from StreamDeck.Devices.StreamDeck import StreamDeck

from data.page import Page


class Profile:
    def __init__(self, deck: StreamDeck):
        self.pages: List[Page] = [Page(0, deck)]
        self.page_number: int = 0
        self.deck: StreamDeck = deck
        self.callback_queue: dict[int, Callable[[StreamDeck, Callable[[int], None]], None]] = {}
        deck.set_key_callback(self.callback)

    def reload(self):
        self.pages[self.page_number].reload()

    def callback(self, _, key: int, state: bool):
        if state:
            print("++Pressed button {} on page {}".format(key, self.page_number))
            self.callback_queue[key] = self.pages[self.page_number].keys[key].press()
        else:
            print("--Released button {} on page {}".format(key, self.page_number))
            self.callback_queue[key](self.deck, self._change_page)
            self.pages[self.page_number].keys[key].reload()

    def _change_page(self, number: int):
        self.page_number = number
        self.reload()

    def load_pages(self, pages):
        self.pages.clear()
        for page in pages:
            self.pages.append(Page(page.number, self.deck))
            self._load_keys(page)

    def _load_keys(self, database_page):
        page: Page = self.pages[database_page.number]
        page_keys = database_page.keys
        for key in page_keys:
            page.keys[key.position].load(key)
        self.reload()
