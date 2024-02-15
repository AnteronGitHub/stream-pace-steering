docker_base_image  := anterondocker/sparse-framework
py_sources 			   := $(shell find . -iname '*.py')

docker_build_file  := .DOCKER
docker_image       := anterondocker/splitnn

ifneq (,$(shell uname -a | grep tegra))
	docker_tag=l4t-pytorch
else
	docker_tag=pytorch
endif

$(docker_build_file): $(py_sources)
	docker build . --build-arg TAGNAME=$(docker_tag) \
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

