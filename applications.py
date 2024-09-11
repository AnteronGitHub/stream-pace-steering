import logging

from sparse_framework import SparseSource, SparseSink, SparseOperator

import torch
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision import transforms

from .vgg import VGG_unsplit

class SparsePyTorchSink(SparseSink):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("SparsePyTorchSink")

    def tuple_received(self, new_tuple):
        self.logger.info("Result: {}".format(new_tuple))

class SparsePyTorchOperator(SparseOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = VGG_unsplit()

    def call(self, input_tuple):
        return self.model(input_tuple)

class SparsePyTorchArgMax(SparseOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(use_batching = False, *args, **kwargs)

    def call(self, input_tuple):
        return torch.argmax(input_tuple)

