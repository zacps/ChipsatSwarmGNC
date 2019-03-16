from cpc.cpc import *
import board
from digitalio import DigitalInOut, Direction
import time

class RoutingNode:
    SYNC_WORD      = "666A"
    HEADER_SYNC    = 0x80
    HEADER_MESSAGE = 0x81
    PACKET_SIZE    = 8

    def __init__(self):
        # Initialization.
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        cs = DigitalInOut(board.radioCS)
        gdo0 = DigitalInOut(board.WAKE)
        # Create an instance to send and receive.
        # SPI object, Chip Select Pin, baudrate, frequency in Hz, Syncword
        self.tx = CC1101(spi, cs, gdo0, 50000, 433920000, self.SYNC_WORD)

        self.rank = 255
        self.last_seen_id = 255

        self.sending = False
        self.receiving = False

        self.led = DigitalInOut(board.LED)
        self.led.direction = Direction.OUTPUT

        # self.message is non-empty iff this chipsat has sent a message but hasn't
        # received a response yet
        self.message = bytearray([])

        self.last_sent_time = 0.0

        self.last_on_poll = time.monotonic()
        self.poll_interval = 8.4

    def on_received_data(self, data):
        self.process_message(data)

    def on_poll(self):
        pass

    def blink(self, n):
        for _ in range(n):
            self.led.value = 1
            time.sleep(0.3/n)
            self.led.value = 0
            time.sleep(0.3/n)

    def send(self, data):
        if not self.sending:
            self.tx.setupTX()
            self.tx.setupCheck()
            self.sending = True
            self.receiving = False

        data_padded = bytearray(self.PACKET_SIZE)
        for i, byte in enumerate(data):
            data_padded[i] = byte

        print("TX", data)
        self.tx.sendRawData(data, self.SYNC_WORD)

    def recv(self, timeout=999999):
        if not self.receiving:
            self.tx.setupRX()
            self.tx.setupCheck()
            self.sending = False
            self.receiving = True

        data = self.tx.receiveRawData(self.PACKET_SIZE, timeout=timeout)
        if data != bytearray([0] * self.PACKET_SIZE):
            print("RX", ':'.join('{:>08b}'.format(i) for i in data))
        return data

    def poll(self):
        try:
            while True:
                data = self.recv(timeout=0.1)
                if data[0]:
                    self.on_received_data(data)

                if time.monotonic() - self.last_on_poll > self.poll_interval:
                    self.on_poll()
                    self.last_on_poll = time.monotonic()

                if time.monotonic() - self.last_sent_time >= 3 and len(self.message) > 0:
                    # Resend after a second if we haven't got an ACK
                    self.send_message()
                    self.last_sent_time = time.monotonic()
        except KeyboardInterrupt:
            self.message = bytearray(input('> ').encode('utf-8'))
            self.send_message()
            self.last_sent_time = time.monotonic()
            self.poll()

    def send_message(self):
        """Send a message back to master.  The message should be contained in self.message."""
        data = bytearray(len(self.message) + 2)
        data[0] = self.HEADER_MESSAGE
        data[1] = self.rank - 1
        data[2:] = self.message
        self.blink(2)
        self.send(data)

    def process_message(self, data):
        if data[0] == self.HEADER_SYNC:
            self.process_sync_message(data)
        elif data[0] == self.HEADER_MESSAGE:
            recv_rank = data[1]
            if recv_rank == self.rank:
                # This message is for us!
                self.message += data[2:]
                self.forward_message()
            elif recv_rank == (self.rank - 2) % 256:
                # Basically an ACK
                self.message = bytearray([])

    def forward_message(self):
        # message format is <header:8><recv_rank:8><data:*>
        data = bytearray(len(self.message) + 2)
        data[0] = self.HEADER_MESSAGE
        data[1] = (self.rank - 1) % 256
        data[2:] = self.message

        if self.rank == 0:
            self.blink(4)
            print('Master received', bytes(self.message))
            self.message = bytearray([])

        print("Forwarding message", data[2:])

        self.blink(1)
        self.send(data)

    def broadcast_sync(self, message_id):
        print("Broadcasting sync")
        self.tx.setupTX()
        self.tx.setupCheck()

        data = bytearray()
        data.append(self.HEADER_SYNC)
        data.append(message_id)
        data.append(self.rank)

        self.blink(3)

        self.send(data)

    def process_sync_message(self, data):
        assert data[0] == self.HEADER_SYNC

        message_id = data[1]

        print("Received sync")

        if (message_id - self.last_seen_id - 1) % 256 >= 128:
            # We've already seen this sync message, ignore it
            print("Already seen, skipping")
            return

        print("Updating rank to", data[2] + 1)
        self.last_seen_id = message_id

        self.rank = data[2] + 1
        self.broadcast_sync(message_id)

