import os

from sparse_framework import SparseAPIClient

if __name__ == "__main__":
    app = { "name": "stream_pace_steering",
            "dag": {
                "SparsePyTorchSource": {"SparsePyTorchOperator"},
                "SparsePyTorchOperator": {"SparsePyTorchArgMax"},
                "SparsePyTorchArgMax": {"SparsePyTorchSink"}
                }
            }
    api_host = os.environ.get('SPARSE_API_HOST') or '127.0.0.1'
    api_port = os.environ.get('SPARSE_API_PORT') or 50006
    SparseAPIClient(api_host, api_port).upload_app(app)
