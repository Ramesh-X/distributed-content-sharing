class Node:
    def __init__(self, ip: str, port: int, name: str, bs_ip: str, bs_port: int) -> None:
        self.ip = ip
        self.port = port
        self.bs_ip = bs_ip
        self.bs_port = bs_port
        self.name = name
    
    def register(self) -> None:
        pass
