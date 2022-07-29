import random
import string
import socket
from typing import List, Optional, Tuple

from peer import Peer
from logger import log_printer

log = log_printer('util')

def id_generator(size=6, chars=string.ascii_uppercase + string.digits) -> str:
    return ''.join(random.choice(chars) for _ in range(size))

def append_len(msg: str) -> str:
    l = len(msg) + 5
    return f'{l:04d} {msg}'

def raise_error(err: str):
    log(f'Error: {err}')
    raise RuntimeError(err)

def validate_response(data: str, min_tokens: int, cmd: str) -> Tuple[List[str], Optional[str]]:
    tokens = data.split()
    if min_tokens < 2:
        min_tokens = 2
    if len(tokens) < min_tokens:
        return tokens, 'Response is too short.'
    if not tokens[0].isdigit():
        return tokens, 'Response first token is not a number.'
    l = int(tokens[0])
    if l != len(data):
        return tokens, 'Response length does not match.'
    if tokens[1] != cmd:
        return tokens, 'Response command does not match.'
    return tokens, None

def send(msg: str, peer: Peer, should_append_len=True, wait_for_response=True, conn=None) -> None:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) if conn is None else conn
    if should_append_len:
        msg = append_len(msg)
    log(f'Sending: "{msg}" to {peer}')
    s.sendto(msg.encode(), peer.as_tuple())
    data = ""
    if wait_for_response:
        data = s.recv(10000).decode('ascii')
    if conn is None:
        s.close()
    log(f'Sent! Received: "{data}"')
    return data
