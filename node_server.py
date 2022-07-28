from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import socket
import time

from node import Node
from file_server import FileServer
from peer import Peer
from util import validate_response, send

MAX_HOPS = 20


class NodeWorker:

    def __init__(self, data: str, peer: Peer, node: Node, file_server: FileServer, s):
        self.data = data
        self.peer = peer
        self.node = node
        self.file_server = file_server
        self.s = s

    def send_ok(self):
        send('OK', self.peer, wait_for_response=False, conn=self.s)

    def run(self):
        data = self.data
        print(f'Received: "{data}"')
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

        toks, error = validate_response(data, 2, 'OK')
        if not error:
            self.send_ok()
            return
        
        toks, error = validate_response(data, 2, 'ROUTE')
        if not error:
            peers_str = self.node.peers_str()
            if peers_str == '':
                print('No peers.')
            else:
                print('###### Peers ######')
                print(peers_str)
                print('###################')
            self.send_ok()
            return
        
        toks, error = validate_response(data, 2, 'FILES')
        if not error:
            files = '\n'.join(self.file_server.file_names)
            if files == '':
                print('No files.')
            else:
                print('###### Files ######')
                print(files)
                print('###################')
            self.send_ok()
            return

        toks, error = validate_response(data, 7, 'SER')
        if not error:
            self.send_ok()
            if self.node.failed:
                return
            respond_to = Peer(toks[2], int(toks[3]))
            hop = int(toks[4])
            search_key = toks[5]
            query = ' '.join(toks[6:])
            if hop >= MAX_HOPS:
                return
            if self.file_server.already_search_for(search_key):
                return
            files = self.file_server.search(query, search_key)
            self.node.files_found(files, respond_to, hop+1, search_key)
            self.node.search_file(query, respond_to, hop+1, search_key)
            return

        toks, error = validate_response(data, 7, 'SEROK')
        if not error:
            self.send_ok()
            file_count = int(toks[2])
            found_in = Peer(toks[3], int(toks[4]))
            hop = int(toks[5])
            search_key = toks[6]
            files = ' '.join(toks[7:]).split(',')
            print(f'Found {file_count} files in {found_in} at hop {hop} with search key: {search_key} at: {time.time_ns()} ns.')
            if file_count > 0:
                print('###### Files ######')
                print('\n'.join(files))
                print('###################')
            return
        
        toks, error = validate_response(data, 3, 'DOWN')
        if not error:
            file_url = self.file_server.download_file(' '.join(toks[2:]))
            if file_url is None:
                msg = 'DOWNOK 1'
            else:
                msg = f'DOWNOK 0 {file_url}'
            send(msg, self.peer, wait_for_response=False, conn=self.s)
            return

        print('Error while processing the received!')


class NodeServer(Thread):

    def __init__(self, node: Node, file_server: FileServer) -> None:
        super().__init__()
        self.node = node
        self.file_server = file_server
        self.executor = ThreadPoolExecutor(max_workers=1)

    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(5)
            print('Listening on node server', self.node.me)
            s.bind((self.node.me.ip, self.node.me.port))
            while True:
                try:
                    data, addr = s.recvfrom(10000)
                    peer = Peer(*addr)
                    worker = NodeWorker(data.decode('ascii'), peer, self.node, self.file_server, s)
                    self.executor.submit(worker.run)
                except:
                    if self.node.connected == False:
                        self.executor.shutdown(wait=True)
                        return
                    continue
