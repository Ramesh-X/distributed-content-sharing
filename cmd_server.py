from threading import Thread

from node import Node

class CMDServer(Thread):
    def __init__(self, node: Node) -> None:
        super().__init__()
        self.node = node
    
    def run(self) -> None:
        while(True):
            x = input("> ")
            if x is None:
                continue
            x = x.strip()
            if x == "":
                continue

            if x == 'list_peers':
                l = [f'{i}: {j}' for i, j in enumerate(self.node.peers)]
                if len(l) == 0:
                    print("No peers.")
                print('\n'.join(l))
            elif x == 'disconnect' or x == 'exit' or x == 'stop' or x == 'quit' or x == 'q':
                self.node.disconnect()
                return
            elif x.startswith('join_to '):
                pid = int(x.split(' ')[1])
                peer = self.node.peers[pid]
                self.node.join_to(peer)
            elif x.startswith('leave_from '):
                pid = int(x.split(' ')[1])
                peer = self.node.peers[pid]
                self.node.leave_from(peer)