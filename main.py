import argparse
from random import randint
from threading import Thread
import time

from peer import Peer
from node import Node
from node_server import NodeServer
from cmd_server import CMDServer
from util import id_generator
from file_server import FileServer
from logger import create_generator

def validate_port(port: int) -> int:
    if port is None or port < 1000 or port > 65535:
        return randint(1000, 65535)
    return port

def main():
    parser = argparse.ArgumentParser(description='File search node for the distributed file search system Bootstrap Server.')
    parser.add_argument('--ip', '-i', type=str, required=True, help='IP address of the node.')
    parser.add_argument('--bs_ip', '-I', type=str, required=True, help='IP address of the Bootstrap Server.')
    parser.add_argument('--port', '-p', type=int, required=False, help='Port to start the node on.')
    parser.add_argument('--bs_port', '-P', type=int, required=True, help='Port to start the Bootstrap Server.')
    parser.add_argument('--file_port', '-f', type=int, required=False, help='Port to start the file server on.')
    parser.add_argument('--name', '-n', type=str, required=False, help='Unique username for the node.')
    parser.add_argument('--cli', '-c', action='store_true', help='Run the node in CLI mode.')

    args = parser.parse_args()
    port = validate_port(args.port)
    file_port = validate_port(args.file_port)
    name = args.name
    if name is None or name == "":
        name = f'node:{port}:{id_generator(4)}'
    create_generator(name)

    me = Peer(args.ip, port)
    bs = Peer(args.bs_ip, args.bs_port)
    node = Node(me, bs, name)

    file_server = FileServer(name, Peer(me.ip, file_port))
    file_server.start()

    node_server = NodeServer(name, node, file_server)
    node_server.start()
    time.sleep(1)

    node_starter = Thread(target=node.connect)
    node_starter.start()
    time.sleep(1)
    

    node_starter.join()
    if args.cli:
        cmd_server = CMDServer(node, file_server)
        cmd_server.start()
        cmd_server.join()
    
    node_server.join()
    file_server.join()

if __name__ == '__main__':
    main()
