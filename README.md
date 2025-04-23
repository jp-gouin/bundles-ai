# GreenDoc - SUSEAI Demo Lab

*Author:* Alessandro Festa

*Rev. Number:* v1.0

SUSE AI Demo enviroment is a simple document that is intended to describe how to implement a local lab to demonstrate capabilites of SUSE AI in the context of specific usecase
This GreenDoc is structured in the following way:

* Cluster setup
* Rancher Fleet setup (for automation of the GreenDoc)
* GreenDoc Configuration
* GreenDoc deployment
* Demo


## Cluster Setup

For the purpose of this GreenDoc we'll use [K3s](https://k3s.io).

### Create namespaces used in the environment

```SHELL
kubectl create namespace cert-manager
```
```SHELL
kubectl create namespace suseai
```

### Create secrets for namespaces

```SHELL
kubectl create secret docker-registry application-collection \
--docker-server=dp.apps.rancher.io \
--docker-username=alessandro.festa1@suse.com \
--docker-password=<INSERT YOUR TOKEN FROM APPCO> \
-n cert-manager
```

```SHELL
kubectl create secret docker-registry application-collection \
--docker-server=dp.apps.rancher.io \
--docker-username=alessandro.festa1@suse.com \
--docker-password=<INSERT YOUR TOKEN FROM APPCO> \
-n suseai
```
```SHELL
kubectl create secret docker-registry application-collection \
--docker-server=dp.apps.rancher.io \
--docker-username=alessandro.festa1@suse.com \
--docker-password=<INSERT YOUR TOKEN FROM APPCO> \
-n fleet-local
```

## Use Rancher Application Collection for components

<!-- ### Deploy cert-manager helm chart

```SHELL
helm upgrade --install cert-manager \
  oci://dp.apps.rancher.io/charts/cert-manager \
  --version 1.17.1 \
  -n cert-manager \
  --create-namespace \
  --set crds.enabled=true \
  --set "global.imagePullSecrets[0].name"="application-collection"
``` -->

### Deploy Rancher Fleet
First let's add the repo if not yet there

```SHELL
helm -n cattle-fleet-system install --create-namespace --wait \
    fleet-crd https://github.com/rancher/fleet/releases/download/v0.12.0/fleet-crd-0.12.0.tgz
```
```SHELL
helm -n cattle-fleet-system install --create-namespace --wait \
    fleet https://github.com/rancher/fleet/releases/download/v0.12.0/fleet-0.12.0.tgz
```
At this point we are ready to pickup the greendoc recipe

## Deploy a minimal SUSEAI Stack with Rancher Fleet

Let's create a minimal github configuration and save it as suseai.yaml

```YAML
apiVersion: fleet.cattle.io/v1alpha1
kind: GitRepo
metadata:
  name: suseai
  # This namespace is special and auto-wired to deploy to the local cluster
  namespace: fleet-local
spec:
  repo: https://github.com/alessandro-festa/bundles
  helmSecretName: basic-auth-secret
  ociRegistry:
    authSecretName: application-collection
  branch: main
  paths:
  - k8s-assistant
```
and add a generic secret for basic authentication

```SHELL
kubectl create secret generic basic-auth-secret \--from-literal=username=alessandro.festa1@suse.com \
--from-literal=password=<INSERT YOUR TOKEN FROM APPCO> \
-n fleet-local
```
Now let's execute the config with kubectl

```SHELL
kubectl apply -f rancher-config.yaml
```
You should have the SUSE AI stack


