import torch
from time import time

from sparse_framework import TaskExecutor
from utils import get_device
from vgg import VGG_unsplit
from memory_buffer import MemoryBuffer

__all__ = ["TensorExecutor"]

class TensorExecutor(TaskExecutor):
    def __init__(self, use_batching : bool, lock, task_queue):
        super().__init__(lock, MemoryBuffer, task_queue)

        self.use_batching = use_batching
        self.device = get_device()
        self.batch_no = 0
        self.model = None

    async def start(self):
        self.model = VGG_unsplit()
        self.logger.info(f"Serving inference for VGG using {self.device} (Batching: {self.use_batching}).")
        await super().start()

    def execute_task(self, callback, lock):
        if self.use_batching:
            features, callbacks, statistics_records = self.memory_buffer.dispatch_batch(lock)
        else:
            features, callbacks, statistics_records = self.memory_buffer.pop_input(lock)

        task_started_at = time()
        pred = self.model(features)
        task_completed_at = time()

        for record in statistics_records:
            record.task_started(task_started_at, self.batch_no)
            record.task_completed(task_completed_at)
        self.batch_no += 1

        callback(pred, callbacks)

