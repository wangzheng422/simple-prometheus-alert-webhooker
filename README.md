# simple-prometheus-alert-webhooker

# wzh

```bash

# podman build -t quay.io/wangzheng422/qimgs:simple-prometheus-alert-webhooker-2024.07.15.v02 -f Dockerfile.ubi9 ./
podman build -t quay.io/wangzheng422/qimgs:simple-prometheus-alert-webhooker-2024.07.15.v03 -f Dockerfile.oc.cli ./

podman push quay.io/wangzheng422/qimgs:simple-prometheus-alert-webhooker-2024.07.15.v03

podman run --name simple-prometheus-alert-webhooker -p 18081:8080 quay.io/wangzheng422/qimgs:simple-prometheus-alert-webhooker-2024.07.15.v03

```