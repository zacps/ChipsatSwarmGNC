from cpc.cpc import *
import time

# Constant syncword.
SYNC_WORD = "DEAD"

# Initialization.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = DigitalInOut(board.radioCS)
gdo0 = DigitalInOut(board.WAKE)

# Create an instance to send and receive.
rx = CC1101(spi, cs, gdo0, 50000, 434400000, SYNC_WORD)
# SPI object, Chip Select Pin, baudrate, frequency in Hz, Syncword

rx.setupTX()
rx.setupCheck()

def send(data):
    # Send data if there's something queued.
    print("Sending", data)
    rx.sendData(data, SYNC_WORD)

while True:
    time.sleep(1)
    send("1101111010101101")

