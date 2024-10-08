import asyncio
import logging
import os

from sparse_framework import SparseSink

class Cifar10LabelLogger(SparseSink):
    def __init__(self, i : int):
        super().__init__()
        self.logger = logging.getLogger(f"Cifar10LabelLogger-{i}")
        logging.basicConfig(format='[%(asctime)s] %(name)s - %(levelname)s: %(message)s', level=logging.INFO)
        self.classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

    def tuple_received(self, new_tuple):
        self.logger.info("Class: %s", self.classes[new_tuple])

async def start_sinks(host : str, no_sources = 10):
    await asyncio.gather(*[Cifar10LabelLogger(i).connect(f"Cifar10Labels-{i}", host) for i in range(no_sources)])

if __name__ == "__main__":
    asyncio.run(start_sinks(os.environ.get("SPARSE_API_HOST") or "127.0.0.1"))
