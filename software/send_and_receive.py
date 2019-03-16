from cpc.cpc import *
import time
import util

# Constant syncword.
SYNC_WORD = "666A"

# Initialization.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = DigitalInOut(board.radioCS)
gdo0 = DigitalInOut(board.WAKE)

# Create an instance to send and receive.
rx = CC1101(spi, cs, gdo0, 50000, 434400000, SYNC_WORD)
# SPI object, Chip Select Pin, baudrate, frequency in Hz, Syncword

rx.setupTX()
rx.setupCheck()

sendBuffer = ["test 123"]
	
def receive():
	# Receive data.
	data = rx.receiveData(1024)
	print(data)
	print(util.from_bits(data))

def send():
	# Send data if there's something queued.
	if len(sendBuffer) != 0:
		rx.sendData(util.to_bits(sendBuffer.pop(0)), SYNC_WORD)

while True:
	send()
	receive()

