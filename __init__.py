from .applications import SparsePyTorchOperator, SparsePyTorchArgMax

def get_operators():
    return [SparsePyTorchOperator, SparsePyTorchArgMax]

def get_sinks():
    return []

