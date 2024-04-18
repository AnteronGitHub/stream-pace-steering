from .applications import SparsePyTorchSource, SparsePyTorchOperator, SparsePyTorchSink

def get_sources():
    return [SparsePyTorchSource]

def get_operators():
    return [SparsePyTorchOperator]

def get_sinks():
    return [SparsePyTorchSink]

