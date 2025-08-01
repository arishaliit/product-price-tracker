Product Price Tracker
This project is a full-stack web application designed to track the price of products from various e-commerce websites. The application consists of a React-based frontend, a Flask-based backend API, and a CI/CD pipeline for automated deployment to a Kubernetes cluster.

Features
Frontend: A user-friendly interface built with React.js that allows users to input a product URL.

Backend: A RESTful API built with Flask and Python for web scraping and data processing.

Containerization: The frontend and backend services are containerized using Docker.

Orchestration: The services are deployed and managed on a local Kubernetes cluster using Minikube.

CI/CD: A GitHub Actions workflow automates the build of Docker images and pushes them to Docker Hub.

Technologies Used
Frontend

React

HTML5, CSS3

Backend

Python

Flask

Infrastructure & DevOps

Kubernetes (Minikube)

Docker

Nginx (as a reverse proxy)

GitHub Actions

How to Run the Project Locally
Follow these steps to set up and run the application on your local machine using Minikube.

Prerequisites
You need to have the following software installed:

Docker: For containerization.

Minikube: To run a local Kubernetes cluster.

kubectl: To interact with the Kubernetes cluster.

Git: To clone the repository.

1. Clone the Repository
Clone the project from GitHub to your local machine:

git clone https://github.com/arishaliit/product-price-tracker.git
cd product-price-tracker


2. Start Minikube
Start your Minikube cluster with a Docker driver. This command may require administrator privileges.

minikube start --driver=docker


3. Build and Push Docker Images
You need to build the Docker images for both the frontend and backend and push them to Docker Hub. First, configure your Docker environment to use Minikube's Docker daemon.

minikube -p minikube docker-env
# Follow the instructions given by the command above to configure your shell
# e.g., on Windows PowerShell:
# & minikube -p minikube docker-env | Invoke-Expression

# Build the images
docker build -t aali25/product-price-tracker-frontend:latest -f Dockerfile.frontend .
docker build -t aali25/product-price-tracker-backend:latest -f Dockerfile.backend .


4. Deploy to Kubernetes
Apply the Kubernetes YAML files to deploy the services and deployments. These files will pull the images from your Docker Hub repository.

kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml


5. Access the Application
To access the frontend, you need to use minikube tunnel to expose the NodePort service.

Open a new terminal window (keep the current one open).

Run the tunnel command in the new terminal. This terminal must remain open.

minikube tunnel



In your original terminal, get the URL for your frontend service:

minikube service frontend-service --url



Copy the URL (e.g., http://127.0.0.1:53212) and open it in your web browser.

Project Structure
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
