import asyncio

from torch.utils.data import DataLoader

from sparse_framework import SparseProtocol
from sparse_framework.stats import ServerRequestStatistics, ClientRequestStatistics

class InferenceClientProtocol(SparseProtocol):
    """Protocol for serving models over a TCP connection.
    """
    def __init__(self,
                 dataset,
                 on_con_lost,
                 no_samples,
                 use_scheduling,
                 target_latency,
                 stats_queue = None):
        super().__init__(stats_queue = stats_queue, request_statistics_factory = ClientRequestStatistics)
        self.dataloader = DataLoader(dataset, 1)
        self.on_con_lost = on_con_lost
        self.no_samples = no_samples
        self.target_latency = target_latency
        self.use_scheduling = use_scheduling

    def connection_made(self, transport):
        super().connection_made(transport)

        self.offload_task()

    def offload_task(self):
        self.current_record = self.request_statistics.create_record("offload_task")
        self.current_record.processing_started()
        self.no_samples -= 1
        features, labels = next(iter(self.dataloader))
        self.send_payload({ 'op': 'offload_task',
                            'activation': features })
        self.current_record.request_sent()

    def payload_received(self, payload):
        self.current_record.response_received()
        self.request_statistics.log_record(self.current_record)
        offload_latency = self.request_statistics.get_offload_latency(self.current_record)

        if (self.no_samples > 0):
            if self.use_scheduling and 'sync' in payload.keys():
                sync = payload['sync']
            else:
                sync = 0.0
            loop = asyncio.get_running_loop()
            loop.call_later(self.target_latency-offload_latency + sync if self.target_latency > offload_latency else 0, self.offload_task)
        else:
            self.transport.close()

    def connection_lost(self, exc):
        self.on_con_lost.set_result(self.request_statistics)

class InferenceServerProtocol(SparseProtocol):
    def __init__(self,
                 task_executor,
                 use_scheduling : bool,
                 use_batching : bool,
                 stats_queue):
        super().__init__(stats_queue = stats_queue, request_statistics_factory = ServerRequestStatistics)

        self.task_executor = task_executor

        self.use_scheduling = use_scheduling
        self.use_batching = use_batching

    def payload_received(self, payload):
        self.current_record = self.request_statistics.create_record(payload["op"])
        self.current_record.request_received()

        self.task_executor.buffer_input(payload["activation"], self.forward_propagated, self.current_record)

    def forward_propagated(self, result, batch_index = 0):
        payload = { "pred": result }
        if self.use_scheduling:
            # Quantize queueing time to millisecond precision
            queueing_time_ms = int(self.request_statistics.get_queueing_time(self.current_record) * 1000)

            # Use externally measured median task latency
            task_latency_ms = 9

            # Use modulo arithmetics to spread batch requests
            sync_delay_ms = batch_index * task_latency_ms + queueing_time_ms % task_latency_ms

            self.current_record.set_sync_delay_ms(sync_delay_ms)
            payload["sync"] =  sync_delay_ms / 1000.0

        self.send_payload(payload)

        self.current_record.response_sent()
        self.request_statistics.log_record(self.current_record)

    def connection_lost(self, exc):
        self.logger.info(self.request_statistics)

        super().connection_lost(exc)
