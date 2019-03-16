from routing_node import RoutingNode
import time

class MasterNode(RoutingNode):
    def __init__(self):
        RoutingNode.__init__(self)
        self.rank = 0
        self.last_seen_id = 0
        self.poll_interval = 10.0
        self.last_on_poll = 0.0

    def on_poll(self):
        self.last_seen_id += 1
        self.broadcast_sync(self.last_seen_id)
