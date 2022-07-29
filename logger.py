from typing import Any, Callable
from pathlib import Path
from time import time
import logging
import sys


class _LogGenerator:

    def __init__(self) -> None:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(threadName)s - %(message)s')
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.stream_handler.setFormatter(formatter)
        Path('logs/').mkdir(parents=True, exist_ok=True)
        t = str(int(time() * 10))[-9:]
        self.file_handler = logging.FileHandler(f'logs/{t}.log',
                                                encoding='utf8')
        self.file_handler.setFormatter(formatter)

    def create_logger(self, name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.stream_handler)
        logger.addHandler(self.file_handler)
        return logger


_generator = _LogGenerator()


def log_printer(name: str) -> Callable[[Any], None]:
    logger = _generator.create_logger(name)

    def func(*msgs: Any) -> None:
        msgs = [f'{msg}' for msg in msgs]
        logger.info(' '.join(msgs))

    return func
