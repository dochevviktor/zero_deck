import serial

SEND_TEXT_COMMAND = b'\x01'
KEY_PRESS_COMMAND = b'\x02'


def send_text_over_serial(command: str):
    ser = serial.Serial("/dev/serial0")
    ser.write(SEND_TEXT_COMMAND + command.encode())
    print("Sending text over Serial {}".format(command))
    ser.close()


def send_key_press_over_serial(command: str):
    ser = serial.Serial("/dev/serial0")
    ser.write(KEY_PRESS_COMMAND + command.encode())
    print("Sending key press over Serial {}".format(command))
    ser.close()
