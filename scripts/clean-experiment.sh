#!/bin/bash

delete_resource () {
  sudo kubectl delete --ignore-not-found -f k8s/$1$2.yaml
}

delete_pods () {
  delete_resource "datasource" $SPARSE_ENVIRONMENT_SUFFIX
  delete_resource "worker_deployment" $SPARSE_ENVIRONMENT_SUFFIX
  if [ $SPARSE_DATASOURCE_USE_EXTERNAL_LINK == "yes" ]; then
    delete_resource "worker_nodeport"
  else
    delete_resource "worker_clusterip"
  fi
}

delete_pods
