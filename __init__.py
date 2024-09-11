from .applications import SparsePyTorchOperator, SparsePyTorchArgMax, SparsePyTorchSink

def get_operators():
    return [SparsePyTorchOperator, SparsePyTorchArgMax]

def get_sinks():
    return [SparsePyTorchSink]

