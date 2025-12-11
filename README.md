# Three Tier DevOps Project — SimplyFi Softech (Task 1, Task 2, Task 3)

## 📌 Project Overview

This project implements a complete **3-tier web application** consisting of:

- **Frontend** → Nginx + HTML/JavaScript  
- **Backend** → Python Flask REST API  
- **Database** → MongoDB  

The project fulfills **all 3 tasks** required by SimplyFi Softech:

| Task | Description |
|------|-------------|
| **Task 1** | Containerize a multi-service application using Dockerfiles |
| **Task 2** | Build and optimize Docker Compose with healthchecks, .env, networks, volumes |
| **Task 3** | Deploy the full application to Kubernetes using kubeadm |

---

# ------------------------------------------------------------
# 🟦 SECTION 1 — Create Project Structure (Local Machine)
# ------------------------------------------------------------

### 1. Create main project directory

```bash
mkdir project3tier
cd project3tier
mkdir backend frontend mongodb k8s

