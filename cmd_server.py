from threading import Thread

from node import Node
from peer import Peer
from file_server import FileServer

class CMDServer(Thread):
    def __init__(self, node: Node, file_server: FileServer) -> None:
        super().__init__()
        self.node = node
        self.file_server = file_server
    
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
                    print('No peers.')
                print(peers_str)
                continue

            if x == 'print_files':
                files = '\n'.join(self.file_server.file_names)
                if files == '':
                    print('No files.')
                print(files)
                continue

            if x == 'disconnect' or x == 'exit' or x == 'stop' or x == 'quit' or x == 'q':
                self.node.disconnect()
                self.file_server.stop()
                return
            
            if x.startswith('? '):
                if len(x) < 4:
                    print('Invalid query.')
                    continue
                self.node.search_file(x[2:])
                continue

            if x == 'toggle_failed':
                self.node.failed = not self.node.failed
                status = 'failed' if self.node.failed else 'not failed'
                print(f'Node status set to {status}.')
                continue

            if ' ' in x:
                pid = int(x.split(' ')[1])
                if pid >= len(self.node.peers) or pid < 0:
                    print('Invalid peer id.')
                    continue
                peer = self.node.peers[pid]
                self.node_command(x, peer)
