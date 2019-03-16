from cpc.cpc import *
import time

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

def to_bits(s):
	result = []
	print("Converting to bits the string: ")
	print(s)
	for c in s:
		bits = bin(ord(c))[2:]
		bits = '00000000'[len(bits):] + bits
		result.extend([str(b) for b in bits])
	result = ''.join(result)
	print("Converted bitstring: ")
	print(result)
	return result

def from_bits(bits):
	bits = list(map(bits, int))
	chars = []
	for b in range(len(bits) / 8):
		byte = bits[b*8:(b+1)*8]
		chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
	return ''.join(chars)
	
def receive():
	# Receive data.
	data = rx.receiveData(1024)
	print(data)
	print(from_bits(data))

def send():
	# Send data if there's something queued.
	if len(sendBuffer) != 0:
		rx.sendData(to_bits(sendBuffer.pop(0)), SYNC_WORD)

while True:
	send()
	receive()

