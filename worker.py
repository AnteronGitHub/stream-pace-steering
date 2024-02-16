import asyncio

from sparse_framework import SparseNode

from executor import TensorExecutor
from protocols import InferenceServerProtocol
from utils import parse_arguments

if __name__ == '__main__':
    args = parse_arguments()
    use_scheduling = int(args.use_scheduling)==1
    use_batching = int(args.use_batching)==1

    executor_factory = lambda lock, queue: TensorExecutor(use_batching, lock, queue)
    server_protocol_factory = lambda executor, stats_queue: lambda: InferenceServerProtocol(executor, use_scheduling, use_batching, stats_queue)

    asyncio.run(SparseNode(executor_factory=executor_factory, server_protocol_factory=server_protocol_factory).start())
