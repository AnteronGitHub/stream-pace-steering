docker_base_image  := anterondocker/sparse-framework
py_sources 			   := $(shell find . -iname '*.py')

docker_build_file  := .DOCKER
docker_image       := anterondocker/stream-pace-steering

ifneq (,$(shell uname -a | grep tegra))
	docker_base_image=nvcr.io/nvidia/l4t-pytorch:r34.1.0-pth1.12-py3
	docker_tag=l4t-pytorch
else
	docker_base_image=pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime
	docker_tag=pytorch
endif

$(docker_build_file): $(py_sources)
	docker build . --build-arg BASE_IMAGE=$(docker_base_image) \
		-t $(docker_image):$(docker_tag)
	touch $(docker_build_file)

.PHONY: docker clean run clean-experiment

docker: $(docker_build_file)

run:
	scripts/run-experiment.sh $(docker_tag)

clean-experiment:
	scripts/clean-experiment.sh

clean:
	sudo rm -f $(docker_build_file)

