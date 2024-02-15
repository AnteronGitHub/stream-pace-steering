# SplitNN
This repository includes an example application for using SplitNN (also called pipeline parallelism) to distribute
inference with a neural network.

The application has been tested with the following devices and the following software:

| Device            | JetPack version | Python version | PyTorch version | Docker version | Base image                                     | Docker tag suffix |
| ----------------- | --------------- | -------------- | --------------- | -------------- | ---------------------------------------------- | ------------------ |
| Jetson AGX Xavier | 5.0 preview     | 3.8.10         | 1.12.0a0        | 20.10.12       | nvcr.io/nvidia/l4t-pytorch:r34.1.0-pth1.12-py3 | jp50               |
| Lenovo ThinkPad   | -               | 3.8.12         | 1.11.0          | 20.10.15       | pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime | amd64              |

# Development with Kubernetes

## Set up paths

```
sudo ln -s $PWD /opt
```

## Initialize experiment

```
source scripts/init-experiment.sh
```

## Run experiment

```
make run
```

## Clean experiment

```
make clean-experiment
```
