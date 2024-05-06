from .applications import SparsePyTorchSource, SparsePyTorchOperator, SparsePyTorchArgMax, SparsePyTorchSink

def get_sources():
    return [SparsePyTorchSource]

def get_operators():
    return [SparsePyTorchOperator, SparsePyTorchArgMax]

def get_sinks():
    return [SparsePyTorchSink]

