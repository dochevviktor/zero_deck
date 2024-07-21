import threading

from StreamDeck.DeviceManager import DeviceManager

from util import database as db
from data.profile import Profile

if __name__ == "__main__":
    streamdeck_list = DeviceManager().enumerate()

    print("Found {} Stream Deck(s).\n".format(len(streamdeck_list)))

    for index, deck in enumerate(streamdeck_list):
        # This script only works with devices that have screens.
        if not deck.is_visual():
            continue

        deck.open()
        deck.reset()

        print("Opened '{}' device (serial number: '{}', fw: '{}')".format(
            deck.deck_type(), deck.get_serial_number(), deck.get_firmware_version()
        ))

        # Set initial screen brightness to 60%.
        deck.set_brightness(60)

        # Load from the DB.
        pages = db.load(deck)

        # Create and fill the new profile
        profile = Profile(deck)
        profile.load_pages(pages)

        db.close()

        # Wait until all application threads have terminated (for this example,
        # this is when all deck handles are closed).
        for t in threading.enumerate():
            try:
                t.join()
            except RuntimeError:
                pass
