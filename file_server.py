import random
from typing import List

class FileServer:
    def __init__(self) -> None:
        k = random.randint(3, 5)
        self.file_names = []
        with open('files.txt', 'r') as f:
            self.file_names = [file_name.strip() for file_name in random.sample(f.readlines(), k)]
    
    def search(self, query: str) -> List[str]:
        return [f for f in self.file_names if query.lower() in f.lower()]
        