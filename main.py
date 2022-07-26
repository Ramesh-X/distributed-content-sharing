import argparse
from random import randint

from .node import Node
from .util import id_generator

def main():
    parser = argparse.ArgumentParser(description='File search node for the distributed file search system Bootstrap Server.')
    parser.add_argument('--ip', '-i', type=str, required=True, help='IP address of the node.')
    parser.add_argument('--bs_ip', '-I', type=str, required=True, help='IP address of the Bootstrap Server.')
    parser.add_argument('--port', '-p', type=int, required=False, help='Port to start the node on.')
    parser.add_argument('--bs_port', '-P', type=int, required=True, help='Port to start the Bootstrap Server.')
    parser.add_argument('--name', '-n', type=str, required=False, help='Unique username for the node.')

    args = parser.parse_args()
    port = args.port
    if port is None or port < 1000 or port > 65535:
        port = randint(1000, 65535)
    name = args.name
    if name is None or name == "":
        name = f'node:{port}:{id_generator(4)}'

    Node(args.ip, port, name, args.bs_ip, args.bs_port).start()

if __name__ == '__main__':
    main()
