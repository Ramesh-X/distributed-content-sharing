import random
import string
import socket

def id_generator(size=6, chars=string.ascii_uppercase + string.digits) -> str:
    return ''.join(random.choice(chars) for _ in range(size))

def append_len(msg: str) -> str:
    l = len(msg) + 5
    return f'{l:04d} {msg}'

def send(msg: str, ip: str, port: int, append_len=True, wait_for_response=True) -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    if append_len:
        msg = append_len(msg)
    s.send(msg)
    data = ""
    if wait_for_response:
        data = s.recv(10000)
    s.close()
    return data

