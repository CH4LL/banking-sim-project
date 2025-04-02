# Cloud-Native Banking App Simulator with Automated CI/CD

## Overview

This project simulates core banking operations via a web interface. **Crucially, it serves as a practical demonstration of building and deploying a containerized Python application to Google Cloud Platform (GCP) using a fully automated CI/CD pipeline.** While the front-end currently provides basic interaction, the core focus is the robust infrastructure, containerization strategy, and the automated deployment workflow.

---

**Live Demo:** [https://banking-sim-service-yf2g5wmnaa-lm.a.run.app/]

***Please Note:*** *The live demo showcases the current front-end interface which is intentionally simple at this stage (displays random numbers on button press). The primary technical value and complexity of this project lie in the underlying cloud architecture, the automated CI/CD pipeline configured in GitHub Actions, and the secure deployment process detailed below.*

---

## Architecture & Workflow

This application follows a modern cloud-native pattern:

1.  **Development:** Code is written (Python/Flask backend, HTML/CSS front-end) and managed using Git, hosted on GitHub.
2.  **Containerization:** The application is packaged into a Docker container for consistent environments.
3.  **CI/CD Pipeline (GitHub Actions):** On every push to the `main` branch:
    *   The GitHub Actions workflow is triggered.
    *   A new Docker image is built.
    *   The image is securely pushed to Google Artifact Registry (GAR).
    *   The workflow authenticates to GCP using IAM Identity Federation (Workload Identity Federation).
    *   The new container image is deployed to Google Cloud Run, updating the live service automatically.
4.  **Serving:** Google Cloud Run serves the containerized application over HTTPS, scaling automatically based on traffic.

TL;DR flow:
`[Developer Push] -> [GitHub Repo] -> [GitHub Actions CI/CD] -> [Build Docker Image] -> [Push to Google Artifact Registry] -> [Deploy to Google Cloud Run] -> [User Access via HTTPS]`

## Key Features & Technical Implementation

*   **Automated CI/CD:** Fully automated build, test (can be added later), and deployment pipeline using **GitHub Actions**.
*   **Containerization:** Application packaged with **Docker** for portability and consistency.
*   **Serverless Deployment:** Leverages **Google Cloud Run** for scalable, managed, serverless deployment.
*   **Artifact Management:** Uses **Google Artifact Registry** for secure storage and management of Docker images.
*   **Secure Cloud Integration:** Implemented **GCP IAM** permissions and **Workload Identity Federation** to allow GitHub Actions to securely interact with GCP resources without static keys.
*   **Python Backend:** Developed using **Python** with the **Flask** framework, providing a RESTful API for the front-end.
*   **Infrastructure Configuration:** Involved enabling necessary **GCP APIs**, configuring service accounts, and setting up Cloud Run service parameters.
*   **Version Control:** Rigorous use of **Git** and GitHub for source code management.

## Tech Stack

*   **Programming Languages:** Python, HTML, CSS
*   **Web Framework:** Flask
*   **Containerization:** Docker
*   **Cloud Platform:** Google Cloud Platform (GCP)
*   **GCP Services:**
    *   Cloud Run (Serverless Compute)
    *   Artifact Registry (Container Registry)
    *   Identity and Access Management (IAM)
    *   Workload Identity Federation
    *   Cloud Build API (implicitly enabled for some operations)
*   **CI/CD:** GitHub Actions
*   **Version Control:** Git, GitHub

## How to Run Locally

1.  Clone the repository: `git clone https://github.com/CH4LL/banking-sim-project.git`
2.  Navigate to the project directory: `cd banking-sim-project`
3.  Build the Docker image: `docker build -t banking-sim .`
4.  Run the Docker container (assuming the app runs on port 8080 inside the container): `docker run -p 8080:8080 banking-sim`
5.  Access the application in your browser at `http://localhost:8080`.

## Future Work

*   Integrate the financial models currently under development into the Python backend scripts.
*   Expand the API endpoints and front-end functionality for more realistic banking operations.
*   Implement automated testing (unit, integration) within the CI/CD pipeline.
*   Potentially explore Infrastructure as Code (Terraform) for managing GCP resources.