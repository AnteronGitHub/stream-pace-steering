from sparse_framework import SparseDeployer

if __name__ == "__main__":
    app = { "SparsePyTorchSource": {"SparsePyTorchOperator"}, "SparsePyTorchOperator": {"SparsePyTorchSink"} }
    SparseDeployer(app).deploy()
