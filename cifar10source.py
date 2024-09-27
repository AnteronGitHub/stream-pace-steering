import asyncio
import os

from sparse_framework import SparseSource
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

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

if __name__ == "__main__":
    endpoint_host = os.environ.get("SPARSE_API_HOST")
    asyncio.run(SparsePyTorchSource(stream_alias="Cifar10Source").connect(endpoint_host))
