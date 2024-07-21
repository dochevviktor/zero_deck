# Zero Deck: A basic Stream Deck backend written in Python

## Description
A basic stream deck controller, which can be deployed on a Raspberry Pi Zero and will then pipe keyboard instructions via serial.<br>
Powered by the [python-elgato-streamdeck project](https://github.com/abcminiuser/python-elgato-streamdeck).

## Development Status
Proof of concept stage<br>
Basic features:
- Create and Load profile from SQLite3 database
- Support page to page navigation (unlimited)
- Basic commands, such as Deck brighness control and Exit
- Serial output to a hardcoded serial port
