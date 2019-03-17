from routing_node import RoutingNode
try:
	import adafruit_tcs34725
			
except:
	class SlaveNode(RoutingNode):
		def __init__(self):
			RoutingNode.__init__(self)
else:
	import busio
	import struct
	import board

	class SlaveNode(RoutingNode):
		def __init__(self):
			RoutingNode.__init__(self)
			i2c = busio.I2C(board.SCL, board.SDA)
			self.sensor = adafruit_tcs34725.TCS34725(i2c)

		def on_poll(self):
			lux = self.sensor.lux
			print(lux)
			self.message = bytearray(struct.pack("f",lux))
			self.send_message()