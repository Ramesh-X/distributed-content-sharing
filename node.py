from .util import send, validate_response

class Node:
    def __init__(self, ip: str, port: int, name: str, bs_ip: str, bs_port: int) -> None:
        self.ip = ip
        self.port = port
        self.bs_ip = bs_ip
        self.bs_port = bs_port
        self.name = name
    
    def start(self) -> None:
        pass
    
    def register(self) -> None:
        msg = f'REG {self.ip} {self.port} {self.name}'
        data = send(msg, self.bs_ip, self.bs_port)
        toks, err = validate_response(data, 3, 'REGOK')
        if err is not None:
            raise RuntimeError(err)
        no_nodes = int(toks[2])
        if no_nodes < 0 or no_nodes > 9995:
            raise RuntimeError(f'Invalid number of nodes: {no_nodes}')
        

