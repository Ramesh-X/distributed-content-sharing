from threading import Thread
import socket

from .node import Node
from .util import validate_response


class NodeWorker(Thread):

    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr

    def send_ok(self):
        self.conn.send(f'0007 OK')

    def process(self):
        data = self.conn.recv(10000)
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
        self.node = node

    def initialize(self) -> None:
        self.node.start()

    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.node.me.ip, self.node.me.port))
            s.listen()
            while True:
                conn, addr = s.accept()
                NodeWorker(conn, addr).start()
