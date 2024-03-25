import uuid

import torch
from torch.utils.data import DataLoader

from vgg import VGG_unsplit

class SparseSource:
    def __init__(self, dataset):
        self.dataloader = DataLoader(dataset, 1)

    def get_tuple(self):
        features, labels = next(iter(self.dataloader))
        return features

class SparseStream:
    def __init__(self,
                 protocol,
                 no_samples,
                 target_latency,
                 use_scheduling,
                 dataset):
        self.id = str(uuid.uuid4())
        self.source = SparseSource(dataset)
        self.protocol = protocol

        self.target_latency = target_latency
        self.use_scheduling = use_scheduling
        self.no_samples = no_samples

    def emit(self):
        self.no_samples -= 1
        payload = {'stream_id': self.id, 'activation': self.source.get_tuple()}
        self.protocol.send_payload(payload)

class SparseSink:
    def __init__(self, logger):
        self.logger = logger

    def tuple_received(self, new_tuple):
        self.logger.info("Result: {}".format(torch.argmax(new_tuple['pred'])))

class SparseOperator:
    def __init__(self):
        self.model = VGG_unsplit()

    def call(self, input_tuple):
        return self.model(input_tuple)

