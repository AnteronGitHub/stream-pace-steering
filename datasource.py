import asyncio
import logging
from sparse_framework import SparseNode

from datasets import get_dataset
from protocols import InferenceClientProtocol
from utils import parse_arguments

async def run_datasources(no_datasources, dataset, no_samples, use_scheduling, target_latency):
    logger = logging.getLogger("sparse")

    tasks = []
    for i in range(no_datasources):
        node_id = str(i)
        client_protocol_factory = lambda on_con_lost, stats_queue: \
                                        lambda: InferenceClientProtocol(dataset, \
                                                                        on_con_lost, \
                                                                        no_samples, \
                                                                        use_scheduling, \
                                                                        target_latency, \
                                                                        stats_queue=stats_queue)
        client_protocol_callback = lambda result: logger.info(result)
        datasource = SparseNode(client_protocol_factory=client_protocol_factory,
                                client_protocol_callback=client_protocol_callback,
                                node_id=node_id)
        tasks.append(datasource.start())

    await asyncio.gather(*tasks)

if __name__ == '__main__':
    args = parse_arguments()
    dataset, classes = get_dataset(args.dataset)
    no_datasources = args.no_datasources
    no_samples = int(args.no_samples)
    use_scheduling = int(args.use_scheduling)==1
    target_latency = float(args.target_latency)/1000.0

    asyncio.run(run_datasources(no_datasources, dataset, no_samples, use_scheduling, target_latency))

