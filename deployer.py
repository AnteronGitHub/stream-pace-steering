from sparse_framework import SparseDeployer

if __name__ == "__main__":
    app = { "name": "sparseapp",
            "dag": {
                "SparsePyTorchSource": {"SparsePyTorchOperator"},
                "SparsePyTorchOperator": {"SparsePyTorchArgMax"},
                "SparsePyTorchArgMax": {"SparsePyTorchSink"}
                }
            }
    SparseDeployer(app).deploy()
