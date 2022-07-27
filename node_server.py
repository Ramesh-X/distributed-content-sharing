from threading import Thread
import socket

from node import Node
from peer import Peer
from util import validate_response, append_len


class NodeWorker(Thread):

    def __init__(self, data: str, addr: str, node: Node):
        super().__init__()
        self.data = data
        print(addr)
        self.addr = addr
        self.node = node

    def send_ok(self):
        self.conn.send(f'0007 OK')

    def process(self):
        data = self.conn.recv(10000)
        toks, error = validate_response(data, 4, 'JOIN')
        if not error:
            peer = Peer(toks[2], int(toks[3]))
            if peer in self.node.peers:
                msg = 'JOINOK 9999'
            else:
                self.node.peers.append(peer)
                msg = 'JOINOK 0'
            msg = append_len(msg)
            self.conn.send(msg)
            return

        toks, error = validate_response(data, 4, 'LEAVE')
        if not error:
            peer = Peer(toks[2], int(toks[3]))
            if peer in self.node.peers:
                self.node.peers.remove(peer)
                msg = 'LEAVEOK 0'
            else:
                msg = 'LEAVEOK 9999'
            msg = append_len(msg)
            self.conn.send(msg)
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

    def run(self):
        try:
            self.process()
        finally:
            self.conn.close()


class NodeServer(Thread):

    def __init__(self, node: Node) -> None:
        super().__init__()
        self.node = node

    def start(self):
        super().start()
        self.node.connect()

    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(10)
            s.bind((self.node.me.ip, self.node.me.port))
            while True:
                try:
                    data, addr = s.recvfrom(10000)
                    NodeWorker(data.decode('ascii'), addr, self.node).start()
                except:
                    if not self.node.connected:
                        return
                    continue
