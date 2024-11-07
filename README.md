# 🐧 Ubuntu VM

This is a docker image with Ubuntu and some tools pre-installed (for example: python3 and nodejs).

It's usefull for connecting to `NODO_CFG` Database

---

## 📦 Make a Release
You can use conventional commits on master branch to trigger a new release.

> [!NOTE]
> You can trigger the GitHub Action manually too.

## 🚀 Deploy
To deploy a new image on AKS you have to run helm this command locally:

```shell
helm upgrade --namespace apiconfig --install --values ./helm/values-<env>.yaml  --debug   --wait --timeout 10m0s ubuntu-vm ./helm
```

> [!IMPORTANT]
> Remember to choose an environment (dev, uat, prod)

---

## 🏠 Work Locally

### Prerequisites
- 🐳 Docker
- 💻 Intel CPU

```shell
docker build -t ubuntu-vm .
docker run -d -8080:8080 ubuntu-vm
```
