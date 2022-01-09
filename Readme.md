# Helm chart to build a simple metrics exporter for external URLs status and latency

## Prerequisites

1. Docker hub account.
2. Kubernetes cluster, you can create test cluster with [minikube](https://minikube.sigs.k8s.io/docs/start/).

## Installation Steps

1. Create docker image, and tag it with your username prefix.
    ```bash
    docker build -t infra-task .
    docker tag infra-task:latest <your-username>/infra-task
    ```
2. Login to your docker hub account using command.
   ```docker login````
3. Verify docker login config 
    ```bash
    cat ~/.docker/config.json
    ```
4. Create kubernetes Secret based on existing Docker credentials.
    ```bash
    kubectl create secret generic regcred \
        --from-file=.dockerconfigjson=<path/to/.docker/config.json> \
        --type=kubernetes.io/dockerconfigjson
    ```
5. Verify secret existence.
    ```bash
    kubectl get secret regcred --output=yaml
    ```
6. Push docker image to docker hub
    ```bash
    docker push <your-username>/infra-task:latest
    ```
7. Add your docker repo url and secret to Chart values 
    ```yaml
    image:
    repository: <your-username>/infra-task
    pullPolicy: IfNotPresent
    tag: "latest"

    imagePullSecrets:
    - name: regcred
    ```
8. Install the helm chart to the kubernetes cluster
    ```bash
    helm install infra-task ./infra-task --set service-type=NodePort
    ```
9. Follow helm install output instructions to get access to the service or setup appropriate ingress.
