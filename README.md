# Product Price Tracker

A full-stack web application designed to track product prices from various e-commerce websites. It features a React-based frontend, a Flask-based backend API, and a CI/CD pipeline for automated deployment to a Kubernetes cluster.

---

## Features

- **Frontend**: User-friendly interface built with React.js for submitting product URLs.
- **Backend**: RESTful API built with Flask and Python for web scraping and data processing.
- **Containerization**: Frontend and backend services are containerized using Docker.
- **Orchestration**: Services are deployed and managed on a local Kubernetes cluster via Minikube.
- **CI/CD**: GitHub Actions workflow automates Docker image builds and pushes to Docker Hub.

---

## Technologies Used

### Frontend
- React
- HTML5, CSS3

### Backend
- Python
- Flask

### Infrastructure & DevOps
- Kubernetes (Minikube)
- Docker
- Nginx (reverse proxy)
- GitHub Actions

---

## How to Run the Project Locally

Follow these steps to set up and run the application using Minikube.

### Prerequisites

Make sure the following tools are installed:

- Docker
- Minikube
- kubectl
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/arishaliit/product-price-tracker.git
cd product-price-tracker
```


### 2. Start Minikube
```
minikube start --driver=docker
```
### 3. Build and Push Docker Images
Configure your shell to use Minikube's Docker daemon:
```
minikube -p minikube docker-env
```

Follow the instructions printed by the command above to configure your shell.
Then build the images:
```
docker build -t aali25/product-price-tracker-frontend:latest -f Dockerfile.frontend .
docker build -t aali25/product-price-tracker-backend:latest -f Dockerfile.backend .
```

### 4. Deploy to Kubernetes

Apply the Kubernetes manifests:
```
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
```

### 5. Access the Application
Start a tunnel to expose the NodePort service:
```
minikube tunnel
```


In a separate terminal, get the service URL:
```
minikube service frontend-service --url
```

## Project Structure
```
product-price-tracker/
├── frontend/
│   ├── src/
│   ├── public/
│   └── ...
├── backend/
│   ├── app.py
│   └── ...
├── k8s/
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── backend-deployment.yaml
│   └── backend-service.yaml
├── .github/
│   └── workflows/
│       └── main.yml
├── Dockerfile.frontend
├── Dockerfile.backend
├── nginx/
│   └── nginx.conf
└── README.md
```
