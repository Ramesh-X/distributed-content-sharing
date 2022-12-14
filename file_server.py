from typing import Dict, List, Optional
from pathlib import Path
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import random
import re

from peer import Peer
from util import id_generator
from logger import log_printer


def get_handler_class(files_meta: Dict[str, str]) -> BaseHTTPRequestHandler:

    class RequestHandler(BaseHTTPRequestHandler):

        def file_not_found(self):
            self.send_error(
                404,
                'File not found',
                f'File key given by the URL path ({self.path}) is not found in the server.',
            )

        def do_GET(self):
            file_name = files_meta.get(self.path[1:])
            if file_name is None:
                self.file_not_found()
                return
            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')
            self.send_header('Content-length', Path(file_name).stat().st_size)
            self.send_header('Content-disposition',
                             f'attachment; filename="{Path(file_name).name}"')
            self.end_headers()
            f = open(file_name, 'rb')
            self.wfile.write(f.read())
            f.close()

    return RequestHandler


class FileServer(Thread):

    def __init__(self, name: str, addr: Peer) -> None:
        super().__init__()
        self.log = log_printer('file_server')
        self.file_dir = f'file_store/{name}'
        Path(self.file_dir).mkdir(parents=True, exist_ok=True)
        k = random.randint(3, 5)
        self.file_names = []
        self.files_meta = {}
        self.search_keys = []
        with open('files.txt', 'r') as f:
            self.file_names = [
                file_name.strip()
                for file_name in random.sample(f.readlines(), k)
            ]
        self.addr = addr
        self.server = HTTPServer(addr.as_tuple(),
                                 get_handler_class(self.files_meta))

    def run(self) -> None:
        self.log(f'File server {self.addr} started.')
        self.server.serve_forever()

    def stop(self) -> None:
        self.server.shutdown()
        self.server.server_close()

    def _url_for(self, key: str) -> str:
        return f'http://{self.addr}/{key}'

    def _create_file(self, path: Path) -> str:
        size = random.randint(2 * 1024 * 1024, 10 * 1024 * 1024)
        path.write_text(id_generator(size))
        key = id_generator(10)
        self.files_meta[key] = path.absolute()
        return key

    def download_file(self, filename) -> Optional[str]:
        self.log("Downloading file:", filename)
        if filename not in self.file_names:
            return None
        path = Path(f'{self.file_dir}/{filename}')
        if path.exists():
            for key in self.search_keys:
                if self.search_keys[key] == path.absolute():
                    return self._url_for(key)
        key = self._create_file(path)
        return self._url_for(key)

    def already_search_for(self, key: str) -> bool:
        return key in self.search_keys

    def search(self, query: str, key: str) -> List[str]:
        if key not in self.search_keys:
            self.search_keys.append(key)
        qs = re.split(r'\W+', query.lower())
        file_words = [
            re.split(r'\W+', file_name.lower())
            for file_name in self.file_names
        ]
        ids = [
            i for i in range(len(file_words))
            if all(q in file_words[i] for q in qs)
        ]
        return [self.file_names[i] for i in ids]
