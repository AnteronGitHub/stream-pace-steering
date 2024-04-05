import asyncio

from sparse_framework import SparseNode

from utils import parse_arguments

from applications import SparsePyTorchOperator

if __name__ == '__main__':
    args = parse_arguments()
    use_scheduling = int(args.use_scheduling)==1
    use_batching = int(args.use_batching)==1

    asyncio.run(SparseNode(operator_factory=SparsePyTorchOperator).start())
