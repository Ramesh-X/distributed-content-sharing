from threading import Thread

from .node import Node

class CMSServer(Thread):
    def __init__(self, node: Node) -> None:
        self.node = node
    
    def run(self) -> None:
        while(True):
            x = input("> ")
            if x == 'list peers':
                l = [f'{i}: {j}' for i, j in enumerate(self.node.peers)]
                print('\n'.join(l))
            elif x.beginswith('join_to '):
                pid = int(x.split(' ')[1])
                peer = self.node.peers[pid]
                self.node.join_to(peer)