import asyncio
import os

from sparse_framework import SparseSource
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

class Cifar10Source(SparseSource):
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

async def start_sources(host : str, no_sources = 10):
    sources = [Cifar10Source(f"Cifar10Source-{i}") for i in range(no_sources)]
    await asyncio.gather(*[source.connect(host) for source in sources])

if __name__ == "__main__":
    asyncio.run(start_sources(os.environ.get("SPARSE_API_HOST") or "127.0.0.1"))
