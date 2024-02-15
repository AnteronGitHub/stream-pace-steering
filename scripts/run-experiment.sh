#!/bin/bash

delete_resource () {
  sudo kubectl delete --ignore-not-found -f k8s/$1$2.yaml
}

create_namespace () {
  sudo kubectl create namespace sparse
}

deploy_resource () {
  cat k8s/$1$2.yaml | envsubst | sudo kubectl apply --wait -f -
}

wait_for_deployment () {
  echo "Waiting for deployment '$1' to be available..."
  sudo kubectl wait --namespace sparse --for=condition=Available deploy/$1
}

deploy_nodes () {
  deploy_resource "worker_deployment" $SPARSE_ENVIRONMENT_SUFFIX
  wait_for_deployment "splitnn-worker"
  if [ $SPARSE_DATASOURCE_USE_EXTERNAL_LINK == "yes" ]; then
    deploy_resource "worker_nodeport"
  else
    deploy_resource "worker_clusterip"
  fi

  delete_resource "datasource" $SPARSE_ENVIRONMENT_SUFFIX
  deploy_resource "datasource" $SPARSE_ENVIRONMENT_SUFFIX
}

create_namespace
deploy_nodes
