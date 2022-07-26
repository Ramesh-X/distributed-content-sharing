import random
import string
import socket

def id_generator(size=6, chars=string.ascii_uppercase + string.digits) -> str:
    return ''.join(random.choice(chars) for _ in range(size))


