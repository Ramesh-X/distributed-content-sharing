from threading import Thread
import socket

from node import Node
from peer import Peer
from util import validate_response, send


class NodeWorker(Thread):

    def __init__(self, data: str, peer: Peer, node: Node, s):
        super().__init__()
        self.data = data
        self.peer = peer
        self.node = node
        self.s = s

    def send_ok(self):
        send('OK', self.peer, wait_for_response=False, conn=self.s)

    def run(self):
        data = self.data
        toks, error = validate_response(data, 4, 'JOIN')
        if not error:
            peer = Peer(toks[2], int(toks[3]))
            if peer in self.node.peers:
                msg = 'JOINOK 9999'
            else:
                self.node.peers.append(peer)
                msg = 'JOINOK 0'
            send(msg, self.peer, wait_for_response=False, conn=self.s)
            return

        toks, error = validate_response(data, 4, 'LEAVE')
        if not error:
            peer = Peer(toks[2], int(toks[3]))
            if peer in self.node.peers:
                self.node.peers.remove(peer)
                msg = 'LEAVEOK 0'
            else:
                msg = 'LEAVEOK 9999'
            send(msg, self.peer, wait_for_response=False, conn=self.s)
            return

        if self.peer not in self.node.peers:
            print(f'Received a message ({data}) from unknown peer: {peer}')
            return

        toks, error = validate_response(data, 6, 'SER')
        if not error:
            self.send_ok()
            # search file
            return

        toks, error = validate_response(data, 6, 'SEROK')
        if not error:
            self.send_ok()
            # do something with files
            return

        print(f'Error while processing the received: "{data}"')


class NodeServer(Thread):

    def __init__(self, node: Node) -> None:
        super().__init__()
        self.node = node

    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(10)
            s.bind((self.node.me.ip, self.node.me.port))
            while True:
                try:
                    data, addr = s.recvfrom(10000)
                    peer = Peer(*addr)
                    NodeWorker(data.decode('ascii'), peer, self.node, s).start()
                except:
                    if self.node.connected == False:
                        return
                    continue
