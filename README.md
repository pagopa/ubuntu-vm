# 🐧 Ubuntu VM

This Docker image contains an Ubuntu base with several tools pre-installed, such as Python 3 and Node.js. 

It's usefull for connecting to the `NODO_CFG` database.

---

## 📦 Creating a Release

To trigger a new release, use conventional commits on the master branch.

> [!NOTE]  
> You can also manually trigger the GitHub Action for the release.

## 🚀 Deployment

To deploy a new image on AKS, follow these steps:
1. Update the image version in the helm values file located at `/helm/values-<env>.yaml`.
2. Run the following Helm commands locally:

```shell
kubectl config get-contexts
kubectl config use-context <your-aks-context>
helm dependency build ./helm
helm upgrade --namespace apiconfig --install --values ./helm/values-<env>.yaml --debug --wait --timeout 5m0s ubuntu-vm ./helm
```

> [!IMPORTANT]  
> Make sure to select the correct environment (dev, uat, prod).

---

## 🏠 Working Locally

### Prerequisites
- 🐳 Docker
- 💻 Intel CPU

To build and run the Docker image locally, use the following commands:

```shell
docker build -t ubuntu-vm .
docker run -d -p 8080:8080 ubuntu-vm
```
