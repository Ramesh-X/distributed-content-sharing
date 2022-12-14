from threading import Thread
import time

from node import Node
from peer import Peer
from file_server import FileServer
from logger import log_printer

class CMDServer(Thread):
    def __init__(self, node: Node, file_server: FileServer) -> None:
        super().__init__()
        self.node = node
        self.file_server = file_server
        self.log = log_printer('cmd_server')
    
    def node_command(self, x: str, peer: Peer) -> None:
        if x.startswith('join_to '):
            self.node.join_to(peer)
            return

        if x.startswith('leave_from '):
            self.node.leave_from(peer)
            return

        if x.startswith('print_peers '):
            self.node.print_peers(peer)
            return
        
        if x.startswith('print_files '):
            self.node.print_files(peer)
            return

        if x.startswith('round_trip_time '):
            self.node.round_trip_time(peer)
            return
        
        if x.startswith('download '):
            filename = ' '.join(x.split(' ')[2:])
            self.node.download(peer, filename)
            return
        
    
    def run(self) -> None:
        while(True):
            x = input("> ")
            if x is None:
                continue
            x = x.strip()
            if x == "":
                continue

            if x == 'print_peers':
                peers_str = self.node.peers_str()
                if peers_str == '':
                    self.log('No peers.')
                self.log(peers_str)
                continue

            if x == 'print_files':
                files = '\n'.join(self.file_server.file_names)
                if files == '':
                    self.log('No files.')
                self.log(files)
                continue

            if x == 'disconnect' or x == 'exit' or x == 'stop' or x == 'quit' or x == 'q':
                self.node.disconnect()
                self.file_server.stop()
                return
            
            if x.startswith('? '):
                if len(x) < 4:
                    self.log('Invalid query.')
                    continue
                self.node.search_file(x[2:])
                continue
        
            if x == 'auto_search':
                with open('queries.txt', 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line == '':
                            continue
                        self.node.search_file(line.strip())
                        time.sleep(0.1)
                continue

            if x == 'toggle_failed':
                self.node.failed = not self.node.failed
                status = 'failed' if self.node.failed else 'not failed'
                self.log(f'Node status set to {status}.')
                continue

            if ' ' in x:
                try:
                    pid = int(x.split(' ')[1])
                except:
                    self.log('Invalid value for id.')
                    continue
                if pid >= len(self.node.peers) or pid < 0:
                    self.log('Invalid peer id.')
                    continue
                peer = self.node.peers[pid]
                self.node_command(x, peer)
