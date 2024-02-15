ARG BASE_IMAGE=pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime
FROM $BASE_IMAGE

ARG LIB_PATH=/usr/lib
RUN mkdir -p $LIB_PATH
ENV PYTHONPATH=$PYTHONPATH:$LIB_PATH

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "worker.py"]
