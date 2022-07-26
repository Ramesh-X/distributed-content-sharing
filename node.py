from .util import send, validate_response
from .peer import Peer

class Node:
    def __init__(self, me: Peer, bs: Peer, name: str) -> None:
        self.me = me
        self.bs = bs
        self.name = name
    
    def start(self) -> None:
        pass
    
    def register(self) -> None:
        msg = f'REG {self.me.ip} {self.me.port} {self.name}'
        data = send(msg, self.bs)
        toks, err = validate_response(data, 3, 'REGOK')
        if err is not None:
            raise RuntimeError(err)
        no_nodes = int(toks[2])
        if no_nodes < 0 or no_nodes > 9995:
            raise RuntimeError(f'Invalid number of nodes: {no_nodes}')
        

