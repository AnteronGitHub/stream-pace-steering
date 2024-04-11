import uuid

from sparse_framework import SparseSource, SparseSink, SparseOperator
import torch
from torch.utils.data import DataLoader

from vgg import VGG_unsplit

class SparsePyTorchSource(SparseSource):
    def __init__(self, dataset, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dataloader = DataLoader(dataset, 1)

    def get_tuple(self):
        features, labels = next(iter(self.dataloader))
        return features

class SparsePyTorchSink(SparseSink):
    def tuple_received(self, new_tuple):
        self.logger.info("Result: {}".format(torch.argmax(new_tuple)))

class SparsePyTorchOperator(SparseOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = VGG_unsplit()

    def call(self, input_tuple):
        return self.model(input_tuple)

