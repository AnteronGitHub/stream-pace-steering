import asyncio
from sparse_framework import SparseNode, SparseStream

from datasets import get_dataset
from applications import SparsePyTorchSource, SparsePyTorchSink
from utils import parse_arguments

async def run_datasources(no_datasources, dataset, no_samples, use_scheduling, target_latency):
    tasks = [SparseNode(node_id=str(i)).start(source_factory=lambda: SparsePyTorchSource(dataset, no_samples, target_latency, use_scheduling), \
                                              sink_factory=SparsePyTorchSink) \
                for i in range(no_datasources)]

    await asyncio.gather(*tasks)

if __name__ == '__main__':
    args = parse_arguments()
    dataset, classes = get_dataset(args.dataset)
    no_datasources = args.no_datasources
    no_samples = int(args.no_samples)
    use_scheduling = int(args.use_scheduling)==1
    target_latency = float(args.target_latency)/1000.0

    asyncio.run(run_datasources(no_datasources, dataset, no_samples, use_scheduling, target_latency))

