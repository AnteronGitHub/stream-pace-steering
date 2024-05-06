import uuid

from sparse_framework import SparseSource, SparseSink, SparseOperator

import torch
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision import transforms

from .vgg import VGG_unsplit

class SparsePyTorchSource(SparseSource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dataloader = DataLoader(datasets.CIFAR10(
            root = "/data",
            train = True,
            download = True,
            transform = transforms.Compose([
                transforms.Resize(size=(32, 32)),
                transforms.ToTensor(),
                transforms.Normalize(
                    (0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)
                    )
                ])
            ),
            1)

    def get_tuple(self):
        features, labels = next(iter(self.dataloader))
        return features

class SparsePyTorchSink(SparseSink):
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

