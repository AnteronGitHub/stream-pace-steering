import os

from sparse_framework import Deployment, SparseAPIClient

if __name__ == "__main__":
    sparse_client = SparseAPIClient(os.environ.get('SPARSE_API_HOST') or '127.0.0.1',
                                    os.environ.get('SPARSE_API_PORT') or 50006)

    sparse_client.create_module('./vgg')
    sparse_client.create_deployment(Deployment.from_yaml("vgg-deployment.yaml"))
