import asyncio
import logging
import os

from sparse_framework import SparseSink

class Cifar10LabelLogger(SparseSink):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("Cifar10LabelLogger")
        logging.basicConfig(format='[%(asctime)s] %(name)s - %(levelname)s: %(message)s', level=logging.INFO)
        self.classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

    def tuple_received(self, new_tuple):
        self.logger.info("Class: %s", self.classes[new_tuple])

if __name__ == "__main__":
    asyncio.run(Cifar10LabelLogger().connect("ArgMax", os.environ.get("SPARSE_API_HOST") or "127.0.0.1"))
