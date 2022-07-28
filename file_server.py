from typing import List
import random
import re

class FileServer:
    def __init__(self) -> None:
        k = random.randint(3, 5)
        self.file_names = []
        self.search_keys = []
        with open('files.txt', 'r') as f:
            self.file_names = [file_name.strip() for file_name in random.sample(f.readlines(), k)]
    
    def already_search_for(self, key: str) -> bool:
        return key in self.search_keys
    
    def search(self, query: str, key: str) -> List[str]:
        if key not in self.search_keys:
            self.search_keys.append(key)
        qs = re.split(r'\W+', query.lower())
        file_words = [re.split(r'\W+', file_name.lower()) for file_name in self.file_names]
        ids = [i for i in range(len(file_words)) if all(q in file_words[i] for q in qs)]
        return [self.file_names[i] for i in ids]
        