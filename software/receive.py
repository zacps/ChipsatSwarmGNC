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

rx.setupRX()
rx.setupCheck()

def receive():
    # Send data if there's something queued.
    print("Receiving")
    data = rx.receiveData(2)
    print("Received", data)

while True:
    time.sleep(1)
    receive()

