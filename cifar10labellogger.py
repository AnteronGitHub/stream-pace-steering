import asyncio
import logging
import os

from sparse_framework import SparseSink

class SparsePyTorchSink(SparseSink):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("SparsePyTorchSink")
        logging.basicConfig(format='[%(asctime)s] %(name)s - %(levelname)s: %(message)s', level=logging.INFO)

    def tuple_received(self, new_tuple):
        self.logger.info("Result: {}".format(new_tuple))

if __name__ == "__main__":
    endpoint_host = os.environ.get("SPARSE_API_HOST")
    asyncio.run(SparsePyTorchSink().connect("SparsePyTorchArgMax", endpoint_host))
