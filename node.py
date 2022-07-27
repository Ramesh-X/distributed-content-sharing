from typing import List 
import random

from .util import raise_error, send, validate_response
from .peer import Peer

class Node:
    def __init__(self, me: Peer, bs: Peer, name: str) -> None:
        self.me = me
        self.bs = bs
        self.name = name
    
    def start(self) -> None:
        pass
    
    def register(self) -> List[Peer]:
        print('Registering with Bootstrap Server...')
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
        print('Registered with Bootstrap Server.')
        return peers
    
    def unregister(self) -> None:
        print('Unregistering with Bootstrap Server...')
        msg = f'UNREG {self.me.ip} {self.me.port} {self.name}'
        data = send(msg, self.bs)
        toks, err = validate_response(data, 3, 'UNROK')
        if err is not None:
            raise_error(err)
        value = int(toks[2])
        if value != 0:
            raise_error(f'Invalid return value: {value}')
        print('Unregistered with Bootstrap Server.')
    
    def listen(self) -> None:
        pass

