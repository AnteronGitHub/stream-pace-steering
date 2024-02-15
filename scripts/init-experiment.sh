#!/bin/bash

init_environment () {
  read -p "Use local sparse framework repository (y/N)? " SPARSE_USE_LOCAL_SOURCE
  if [ $SPARSE_USE_LOCAL_SOURCE == "y" ]; then
    export SPARSE_ENVIRONMENT_SUFFIX="_dev"
  else
    export SPARSE_ENVIRONMENT_SUFFIX=""
  fi

  # Experiment specs
  read -p "Model to be used (default VGG): " SPARSE_MODEL
  export SPARSE_MODEL=${SPARSE_MODEL:-VGG}

  read -p "Dataset to be used (default CIFAR10): " SPARSE_DATASET
  export SPARSE_DATASET=${SPARSE_DATASET:-CIFAR10}

  read -p "Number of samples per dataset (default 64): " SPARSE_NO_SAMPLES
  export SPARSE_NO_SAMPLES=${SPARSE_NO_SAMPLES:-64}

  read -p "How many data sources to run (default 1): " SPARSE_NO_DATASOURCES
  export SPARSE_NO_DATASOURCES=${SPARSE_NO_DATASOURCES:-1}

  read -p "Use scheduling (default 1): " SPARSE_USE_SCHEDULING
  export SPARSE_USE_SCHEDULING=${SPARSE_USE_SCHEDULING:-1}

  read -p "Use batching (default 1): " SPARSE_USE_BATCHING
  export SPARSE_USE_BATCHING=${SPARSE_USE_BATCHING:-1}

  read -p "Target latency in milliseconds (default 200): " SPARSE_TARGET_LATENCY
  export SPARSE_TARGET_LATENCY=${SPARSE_TARGET_LATENCY:-200}

  # Deployment specs
  read -p "Use external link for data source (default 'no'): " SPARSE_DATASOURCE_USE_EXTERNAL_LINK
  export SPARSE_DATASOURCE_USE_EXTERNAL_LINK=${SPARSE_DATASOURCE_USE_EXTERNAL_LINK:-"no"}
  if [ $SPARSE_DATASOURCE_USE_EXTERNAL_LINK == "yes" ]; then
    read -p "External IP for downstream link: " SPARSE_DATASOURCE_DOWNSTREAM_HOST
    read -p "Port for downstream link (default 30007): " SPARSE_DATASOURCE_DOWNSTREAM_PORT

    export SPARSE_DATASOURCE_DOWNSTREAM_HOST=$SPARSE_DATASOURCE_DOWNSTREAM_HOST
    export SPARSE_DATASOURCE_DOWNSTREAM_PORT=${SPARSE_DATASOURCE_DOWNSTREAM_PORT:-"30007"}
  else
    export SPARSE_DATASOURCE_DOWNSTREAM_HOST="splitnn-worker"
    export SPARSE_DATASOURCE_DOWNSTREAM_PORT=50007
  fi
}

init_environment
