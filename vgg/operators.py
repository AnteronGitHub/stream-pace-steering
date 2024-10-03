import torch

from sparse_framework import StreamOperator

from .vgg import VGG_unsplit

class VGGClassifier(StreamOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = VGG_unsplit(num_classes=10)

    def call(self, input_tuple):
        return self.model(input_tuple)

class ArgMax(StreamOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(use_batching = False, *args, **kwargs)

    def call(self, input_tuple):
        return torch.argmax(input_tuple)

