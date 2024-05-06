from sparse_framework import SparseNode

if __name__ == "__main__":
    app = { "name": "sparseapp",
            "dag": {
                "SparsePyTorchSource": {"SparsePyTorchOperator"},
                "SparsePyTorchOperator": {"SparsePyTorchArgMax"},
                "SparsePyTorchArgMax": {"SparsePyTorchSink"}
                }
            }
    SparseNode().deploy_app(app)
