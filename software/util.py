# Converts a string s to bits, ready to be passed to cpc.sendData().
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

# Converts a bitstring to a human-readable string.
def from_bits(bits):
	bits = list(map(int, bits))
	chars = []
	for b in range(len(bits) / 8):
		byte = bits[b*8:(b+1)*8]
		chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
	return ''.join(chars)
