# Three Tier DevOps Project — SimplyFi Softech (Task 1, Task 2, Task 3)

## 📌 Project Overview

This project implements a complete **3-tier web application** consisting of:

- **Frontend** → Nginx + HTML/JavaScript  
- **Backend** → Python Flask REST API  
- **Database** → MongoDB  


| Task | Description |
|------|-------------|
| **Task 1** | Containerize a multi-service application using Dockerfiles |
| **Task 2** | Build and optimize Docker Compose with healthchecks, .env, networks, volumes |
| **Task 3** | Deploy the full application to Kubernetes using kubeadm |

---

## 📌 Project Objectives

- Create a structured application
- Secure secrets using `.env`
- Containerize using Docker
- Deploy using Docker Compose
- Automate build & deployment using Jenkins
- Trigger deployment automatically on Git push

---
## 📐 Project Architecture
                        ┌────────────────────┐
                        │     End User       │
                        └─────────┬──────────┘
                                  │ HTTP Request
                        ┌─────────▼──────────┐
                        │ Nginx Reverse Proxy│
                        │  (Routing Layer)   │
                        └─────────┬──────────┘
                  Static Content   │    REST API Calls
            ┌─────────────────────▼──┐   ┌──────────────────┐
            │     Frontend Service   │   │  Backend Service │
            │   (HTML / JS / Nginx)  │   │   (Flask API)    │
            │   Docker Container     │   │ Docker Container │
            └──────────────┬─────────┘   └────────┬─────────┘
                           │                      │
                           │                      │
                   ┌───────▼────────┐    ┌────────▼─────────┐
                   │   Cache Layer  │    │    Database      │
                   │     (Redis)    │    │  PostgreSQL DB   │
                   │Docker Container│    │  Persistent Vol  │
                   └────────────────┘    └──────────────────┘


# ------------------------------------------------------------
# 🟦 SECTION 1 — Create Project Structure (Local Machine)
# ------------------------------------------------------------

### 1. Create main project directory

```bash
mkdir project3tier
cd project3tier
```

### 2. Create folder structure

```bash
mkdir backend frontend mongodb k8s
```

---

# ------------------------------------------------------------
# 🟦 SECTION 2 — Application Code
# ------------------------------------------------------------

## ⭐ Backend (Flask + MongoDB)

### `backend/app.py`

```python
from flask import Flask, jsonify, request
from pymongo import MongoClient
import os

app = Flask(__name__)

MONGO_HOST = os.environ.get("MONGO_HOST", "mongo")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
MONGO_DB = os.environ.get("MONGO_DB", "appdb")

client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
db = client[MONGO_DB]
items = db["items"]

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.get("/items")
def get_items():
    return list(items.find({}, {"_id": 0}))

@app.post("/items")
def add_item():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return {"error": "name is required"}, 400
    item = {"name": name}
    items.insert_one(item)
    return item, 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

### `backend/requirements.txt`

```
Flask
pymongo
```

### `backend/Dockerfile`

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

---

## ⭐ Frontend (HTML + JS)

### `frontend/index.html`

```html
<!DOCTYPE html>
<html>
<body>
  <h1>Three Tier App</h1>
  <input id="name" placeholder="Enter item" />
  <button onclick="addItem()">Add</button>
  <ul id="items"></ul>
<script src="main.js"></script>
</body>
</html>
```

### `frontend/main.js`

```javascript
const API = "/api";

async function load() {
    const r = await fetch(API + "/items");
    const data = await r.json();
    document.getElementById("items").innerHTML =
        data.map(i => `<li>${i.name}</li>`).join("");
}

async function addItem() {
    const name = document.getElementById("name").value;
    await fetch(API + "/items", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name})
    });
    load();
}

load();
```

### `frontend/Dockerfile`

```dockerfile
FROM nginx:alpine
COPY . /usr/share/nginx/html
```

---

## ⭐ MongoDB Image

### `mongodb/Dockerfile`

```dockerfile
FROM mongo:6
EXPOSE 27017
CMD ["mongod"]
```

---

# ------------------------------------------------------------
# 🟦 SECTION 3 — Save Code to Git Remote Repository
# ------------------------------------------------------------

Initialize Git:

```bash
git init
git add .
git commit -m "initial commit"
```

Add remote:

```bash
git remote add origin https://github.com/<username>/<repository>.git
```

Push project:

```bash
git push -u origin main
```

---

# ------------------------------------------------------------
# 🟦 SECTION 4 — Clone Project on Remote Host
# ------------------------------------------------------------

SSH into EC2:

```bash
ssh -i key.pem ubuntu@<EC2-PUBLIC-IP>
```

Become root:

```bash
sudo -i
```

Clone repo:

```bash
git clone https://github.com/<username>/<repository>.git
cd project3tier
```

---

# ------------------------------------------------------------
# 🟦 SECTION 5 — Install Required Software on Remote Host
# ------------------------------------------------------------

Install Docker + Compose:

```bash
apt update -y
apt install -y docker.io docker-compose git
systemctl enable docker --now
```

Give docker permissions:

```bash
usermod -aG docker ubuntu
```

Logout and login again.

---

# ------------------------------------------------------------
# 🟦 SECTION 6 — TASK 1: Containerize the Application
# ------------------------------------------------------------

### ⭐ Build Docker images

```bash
docker build -t backend:latest backend/
docker build -t frontend:latest frontend/
docker build -t mongo-custom:latest mongodb/
```

### ⭐ Run containers

```bash
docker run -d --name mongo -p 27017:27017 mongo-custom:latest
docker run -d --name backend --link mongo -p 5000:5000 backend:latest
docker run -d --name frontend -p 80:80 frontend:latest
```

---

# ------------------------------------------------------------
# 🟦 SECTION 7 — Push Images to Docker Hub
# ------------------------------------------------------------

Login:

```bash
docker login
```

Tag & push:

```bash
docker tag backend:latest blesssedmess/backend:latest
docker push blesssedmess/backend:latest

docker tag frontend:latest blesssedmess/frontend:latest
docker push blesssedmess/frontend:latest

docker tag mongo-custom:latest blesssedmess/mongo:latest
docker push blesssedmess/mongo:latest
```

---

# ------------------------------------------------------------
# 🟦 SECTION 8 — TASK 2: Docker Compose Setup
# ------------------------------------------------------------

Create `.env`:

```env
MONGO_HOST=mongo
MONGO_PORT=27017
MONGO_DB=appdb
BACKEND_PORT=5000
FRONTEND_PORT=80
```

### `docker-compose.yml`

```yaml
version: "3.8"

services:
  mongo:
    image: blesssedmess/mongo:latest
    container_name: mongo
    ports:
      - "${MONGO_PORT}:27017"
    volumes:
      - mongo_data:/data/db
    healthcheck:
      test: ["CMD-SHELL", "mongosh --eval \"db.adminCommand('ping')\""]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    image: blesssedmess/backend:latest
    container_name: backend
    depends_on:
      mongo:
        condition: service_healthy
    ports:
      - "${BACKEND_PORT}:5000"
    environment:
      MONGO_HOST: ${MONGO_HOST}
      MONGO_PORT: ${MONGO_PORT}
      MONGO_DB: ${MONGO_DB}

  frontend:
    image: blesssedmess/frontend:latest
    container_name: frontend
    ports:
      - "${FRONTEND_PORT}:80"

volumes:
  mongo_data:
```

Start services:

```bash
docker compose up -d
```

---

# ------------------------------------------------------------
# 🟦 SECTION 9 — Install Kubernetes (kubeadm)
# ------------------------------------------------------------

Disable swap:

```bash
swapoff -a
sed -i '/swap/d' /etc/fstab
```

Install kubeadm, kubelet, kubectl:

```bash
apt update
apt install -y apt-transport-https ca-certificates curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"
apt update
apt install -y kubelet kubeadm kubectl
```

Initialize cluster:

```bash
kubeadm init --pod-network-cidr=192.168.0.0/16
```

Configure kubectl:

```bash
mkdir -p ~/.kube
cp /etc/kubernetes/admin.conf ~/.kube/config
```

Install Calico:

```bash
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
```

Allow master to run pods:

```bash
kubectl taint nodes --all node-role.kubernetes.io/control-plane-
```

Install Local Path Storage:

```bash
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
kubectl patch storageclass local-path -p '{"metadata":{"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```

Create required directory:

```bash
mkdir -p /opt/local-path-provisioner
chmod 777 /opt/local-path-provisioner
```

---

# ------------------------------------------------------------
# 🟦 SECTION 10 — TASK 3: Deploy Application to Kubernetes
# ------------------------------------------------------------

## Apply ConfigMap & Secret

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
```

## Deploy PVC

```bash
kubectl apply -f k8s/mongo-pvc.yaml
```

## Deploy MongoDB

```bash
kubectl apply -f k8s/mongo-deployment.yaml
kubectl apply -f k8s/mongo-service.yaml
```

## Deploy Backend

```bash
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
```

## Deploy Frontend (NodePort)

```bash
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
```

Access application:

```
http://<EC2-PUBLIC-IP>:30080
```

---

# TASKS COMPLETED SUCCESSFULLY

This project includes:

✔ Dockerfiles  
✔ Docker Compose  
✔ Kubernetes manifests  
✔ Multi-tier architecture  
✔ Fully working deployment  

---
