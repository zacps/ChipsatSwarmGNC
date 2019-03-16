from routing_node import RoutingNode

class SlaveNode(RoutingNode):
    def __init__(self):
        RoutingNode.__init__(self)
        self.sent = False

    def on_received_data(self, data):
        self.process_message(data)
        print('Rank:', self.rank)
        if self.rank != 255 and not self.sent:
            self.send_message(b"CHIP")
            self.sent = True
