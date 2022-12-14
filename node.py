from typing import List, Optional 
import random
import time

from util import id_generator, raise_error, send, validate_response
from peer import Peer
from logger import log_printer
    
class Node:
    def __init__(self, me: Peer, bs: Peer, name: str) -> None:
        self.log = log_printer('node')
        self.me = me
        self.bs = bs
        self.name = name
        self.peers = []
        self.connected = None
        self.failed = False
    
    def peers_str(self) -> str:
        l = [f'{i}: {j}' for i, j in enumerate(self.peers)]
        if len(l) == 0:
            return ''
        return '\n'.join(l)
    
    def connect(self) -> None:
        peers = self.register()
        for peer in peers:
            self.join_to(peer)
        self.connected = True

    def disconnect(self) -> None:
        for peer in list(self.peers):
            self.leave_from(peer)
        self.unregister()
        self.connected = False
    
    def register(self) -> List[Peer]:
        self.log(f'Registering with Bootstrap Server (Details => node: {self.me}, name: {self.name})...')
        msg = f'REG {self.me.ip} {self.me.port} {self.name}'
        data = send(msg, self.bs)
        toks, err = validate_response(data, 3, 'REGOK')
        if err is not None:
            raise_error(err)
        no_nodes = int(toks[2])
        if no_nodes < 0 or no_nodes > 9995:
            raise_error(f'Invalid number of nodes: {no_nodes}')
        peers = [Peer(toks[3 + i * 2], int(toks[4 + i * 2])) for i in range(no_nodes)]
        if no_nodes > 2:
            peers = random.sample(peers, 2)
        self.log('Registered with Bootstrap Server.')
        return peers
    
    def unregister(self) -> None:
        self.log('Unregistering with Bootstrap Server...')
        msg = f'UNREG {self.me.ip} {self.me.port} {self.name}'
        data = send(msg, self.bs)
        toks, err = validate_response(data, 3, 'UNROK')
        if err is not None:
            raise_error(err)
        value = int(toks[2])
        if value != 0:
            raise_error(f'Invalid return value: {value}')
        self.log('Unregistered with Bootstrap Server.')
    
    def join_to(self, peer: Peer) -> None:
        self.log(f'Joining to {peer}...')
        msg = f'JOIN {self.me.ip} {self.me.port}'
        data = send(msg, peer)
        toks, err = validate_response(data, 3, 'JOINOK')
        if err is not None:
            raise_error(err)
        value = int(toks[2])
        if value != 0:
            raise_error(f'Invalid return value: {value}')
        self.peers.append(peer)
        self.log(f'Joined to {peer}.')
    
    def leave_from(self, peer: Peer) -> None:
        self.log(f'Leaving from {peer}...')
        msg = f'LEAVE {self.me.ip} {self.me.port}'
        data = send(msg, peer)
        toks, err = validate_response(data, 3, 'LEAVEOK')
        if err is not None:
            raise_error(err)
        value = int(toks[2])
        if value != 0:
            raise_error(f'Invalid return value: {value}')
        self.peers.remove(peer)
        self.log(f'Left from {peer}.')
    
    def print_peers(self, peer: Peer) -> None:
        self.log(f'Command {peer} to print peers...')
        msg = 'ROUTE'
        data = send(msg, peer)
        _, err = validate_response(data, 2, 'OK')
        if err is not None:
            raise_error(err)
        self.log(f'Print peers command sent to {peer}.')
    
    def print_files(self, peer: Peer) -> None:
        self.log(f'Command {peer} to print files...')
        msg = 'FILES'
        data = send(msg, peer)
        _, err = validate_response(data, 2, 'OK')
        if err is not None:
            raise_error(err)
        self.log(f'Print files command sent to {peer}.')
    
    def round_trip_time(self, peer: Peer) -> int:
        self.log(f'Calculating round trip time to {peer}...')
        t1 = time.time_ns()
        msg = 'OK'
        data = send(msg, peer)
        _, err = validate_response(data, 2, 'OK')
        if err is not None:
            raise_error(err)
        t2 = time.time_ns()
        x = t2-t1
        self.log(f'Measured round trip time to {peer} is {x} ns')
        return x
    
    def search_file(self, query: str, respond_to: Peer=None, hop: int=0, search_key: str=None) -> None:
        if search_key is None:
            search_key = id_generator(6)
        self.log(f'Searching for {query} with key: {search_key} hop: {hop} at: {time.time_ns()} ns...')
        if respond_to is None:
            respond_to = self.me
        msg = f'SER {respond_to.ip} {respond_to.port} {hop} {search_key} {query}'
        for peer in self.peers:
            if peer == respond_to:
                continue
            data = send(msg, peer)
            toks, err = validate_response(data, 2, 'OK')
            if err is not None:
                raise_error(err)
    
    def files_found(self, files: List[str], respond_to: Peer, hop: int, search_key: str) -> None:
        self.log(f'Sending file found command for {len(files)} files with key {search_key}...')
        fs = ','.join(files)
        msg = f'SEROK {len(files)} {self.me.ip} {self.me.port} {hop} {search_key} {fs}'
        data = send(msg, respond_to)
        toks, err = validate_response(data, 2, 'OK')
        if err is not None:
            raise_error(err)
        self.log(f'Files found command sent to {respond_to}.')
    
    def download(self, peer: Peer, filename: str) -> Optional[str]:
        self.log(f'Downloading {filename}...')
        msg = f'DOWN {filename}'
        data = send(msg, peer)
        toks, err = validate_response(data, 3, 'DOWNOK')
        if err is not None:
            raise_error(err)
        value = int(toks[2])
        if value == 0:
            url = toks[3]
            self.log(f'{filename} can be downloaded from {url}.')
            return url
        if value == 1:
            self.log(f'{filename} is not available.')
            return None
        raise_error(f'Invalid return value: {value}')
