from routing_node import RoutingNode
import time

class MasterNode(RoutingNode):
    def __init__(self):
        RoutingNode.__init__(self)
        self.rank = 0
        self.last_seen_id = 0
        self.last_sync_time = 0

    def on_poll(self):
        if time.time() - self.last_sync_time >= 10:
            self.last_seen_id += 1
            self.broadcast_sync(self.last_seen_id)
            self.last_sync_time = time.time()
