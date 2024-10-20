# Rule Engine Application

This project implements a rule engine that utilizes an Abstract Syntax Tree (AST) for dynamic rule evaluation based on user attributes such as age, department, income, and spending. The application allows for the creation, combination, and evaluation of rules to determine user eligibility. The backend is built with Flask, while the frontend uses HTML, CSS, and JavaScript for a user-friendly interface. The application is containerized using Docker for easy setup and deployment.

## Features

- Dynamic rule creation with logical operators (AND, OR).
- Evaluate user eligibility based on defined rules.
- Abstract Syntax Tree (AST) representation for efficient evaluation.
- RESTful API for creating, combining, and evaluating rules.
- Runs in a Docker container for ease of deployment.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)

## Prerequisites

Before setting up the application, ensure you have the following installed:

- Docker
- Docker Compose
- Python 3.x

## Installation

### Clone the Repository

Clone the repository to your local machine:

git clone <repository-url>
cd <project-directory>

## Set Up the Configuration
    Create a file named config.py in the root of your project and add your MongoDB URI like this:

    MONGO_URI = "mongodb://localhost:27017"

## Running the Application
    Using Docker
    Build the Docker image and start the containers:

    docker-compose up --build
## Once the container is running, open your browser and go to:

    http://localhost:5000
## Additionals
  added string validation (parentheses checker)
  
