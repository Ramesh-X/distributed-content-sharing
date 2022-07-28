from typing import Tuple


class Peer:

    def __init__(self, ip: str, port: int) -> None:
        self.ip = ip
        self.port = port

    def as_tuple(self) -> Tuple[str, int]:
        return self.ip, self.port

    def __str__(self) -> str:
        return f'{self.ip}:{self.port}'

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Peer):
            return False
        return self.ip == o.ip and self.port == o.port

    def __hash__(self) -> int:
        return hash((self.ip, self.port))
