import os

from sparse_framework import Deployment, SparseAPIClient

if __name__ == "__main__":
    module_name = "VGGClassifier"
    deployment = Deployment(name="VGGClassifier",
                            dag={"Cifar10Source": {"VGGClassifier"},
                                 "VGGClassifier": {"ArgMax"}})
    api_host = os.environ.get('SPARSE_API_HOST') or '127.0.0.1'
    api_port = os.environ.get('SPARSE_API_PORT') or 50006
    sparse_client = SparseAPIClient(api_host, api_port)

    sparse_client.create_module(module_name, module_dir='./sparse_module')
    sparse_client.create_deployment(deployment)
