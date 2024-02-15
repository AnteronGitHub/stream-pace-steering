import asyncio
import multiprocessing

from sparse_framework import SparseNode

from executor import TensorExecutor
from memory_buffer import MemoryBuffer
from protocols import InferenceServerProtocol
from utils import parse_arguments, get_device

class InferenceServer(SparseNode):
    """A Node serves inference requests for models over a TCP connection.

    Inference server runs the executor in a separate thread from the server, using an asynchronous queue.
    """
    def __init__(self, use_scheduling : bool, use_batching : bool):
        super().__init__()

        self.use_scheduling = use_scheduling
        self.use_batching = use_batching

    def get_futures(self):
        futures = super().get_futures()

        m = multiprocessing.Manager()
        lock = m.Lock()

        task_queue = asyncio.Queue()

        executor = TensorExecutor(self.use_batching, lock, task_queue)
        futures.append(executor.start())
        futures.append(self.start_server(lambda: InferenceServerProtocol(executor, \
                                                                         self.use_scheduling, \
                                                                         self.use_batching, \
                                                                         self.stats_queue), \
                                         self.config.listen_address, \
                                         self.config.listen_port))

        return futures

if __name__ == '__main__':
    args = parse_arguments()

    asyncio.run(InferenceServer(int(args.use_scheduling)==1, int(args.use_batching)==1).start())
