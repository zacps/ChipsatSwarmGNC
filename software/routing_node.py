from cpc.cpc import *
import time

class RoutingNode:
    SYNC_WORD      = "BEEF"
    HEADER_SYNC    = 0x80
    HEADER_MESSAGE = 0x81
    PACKET_SIZE    = 16

    def __init__(self):
        # Initialization.
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        cs = DigitalInOut(board.radioCS)
        gdo0 = DigitalInOut(board.WAKE)
        # Create an instance to send and receive.
        # SPI object, Chip Select Pin, baudrate, frequency in Hz, Syncword
        self.tx = CC1101(spi, cs, gdo0, 50000, 434400000, self.SYNC_WORD)

        self.rank = 255
        self.last_seen_id = 255

        self.sending = False
        self.receiving = False

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

    def recv(self):
        if not self.receiving:
            self.tx.setupRX()
            self.tx.setupCheck()
            self.sending = False
            self.receiving = True

        data = self.tx.receiveRawData(self.PACKET_SIZE)
        print("RX", data)
        return data

    def send_message(self, message):
        data = bytearray(len(message) + 2)
        data[0] = self.HEADER_MESSAGE
        data[1] = self.rank - 1
        data[2:] = message
        self.send(data)

    def process_message(self, data):
        if data[0] == self.HEADER_SYNC:
            self.process_sync_message(data)
        elif data[0] == self.HEADER_MESSAGE:
            self.forward_message(data)

    def forward_message(self, data):
        # message format is <header:8><recv_rank:8><data:*>
        assert data[0] == self.HEADER_MESSAGE

        recv_rank = data[1]
        if recv_rank != self.rank:
            return

        if recv_rank == 0:
            print('Master received', data[2:])
            return

        print("Forwarding message", data[2:])

        data[1] -= 1
        self.send(data)

    def broadcast_sync(self, message_id):
        print("Broadcasting sync")
        self.tx.setupTX()
        self.tx.setupCheck()

        data = bytearray()
        data.append(self.HEADER_SYNC)
        data.append(message_id)
        data.append(self.rank)

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

