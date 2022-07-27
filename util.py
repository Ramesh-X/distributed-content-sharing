from curses.ascii import isdigit
import random
import string
import socket
from typing import List, Optional, Tuple

from .peer import Peer

def id_generator(size=6, chars=string.ascii_uppercase + string.digits) -> str:
    return ''.join(random.choice(chars) for _ in range(size))

def append_len(msg: str) -> str:
    l = len(msg) + 5
    return f'{l:04d} {msg}'

def raise_error(err: str):
    print(f'Error: {err}')
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

def send(msg: str, peer: Peer, append_len=True, wait_for_response=True) -> str:
    print(f'Sending: "{msg}" to {peer}')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((peer.ip, peer.port))
    if append_len:
        msg = append_len(msg)
    s.send(msg)
    data = ""
    if wait_for_response:
        data = s.recv(10000)
    s.close()
    return data

