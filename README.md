# Screenshot Service

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0-green.svg)
![Docker](https://img.shields.io/badge/Docker-3.8-blue.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-4.4-green.svg)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg)

## Table of Contents

- [Screenshot Service](#screenshot-service)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Installation](#installation)
    - [Docker](#docker)
  - [Usage](#usage)
    - [API endpoints](#api-endpoints)
  - [Testing](#testing)
  - [Monitoring](#monitoring)

## Introduction

Screenshot Service is a FastAPI-based web service designed to capture screenshots of web pages and save them to a MongoDB database. The service is highly customizable, supporting asynchronous operations, and is equipped with integrated monitoring and testing tools.

## Features

- Asynchronous screenshot capturing using Pyppeteer.
- MongoDB integration with both local and `mongomock` support.
- Unit and integration tests with pytest.
- Monitoring using Prometheus and Grafana.
- Dockerized setup for easy deployment.
- Redis as a cache server for recurrent websites

## Installation

### Docker

To run the project using Docker, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/screenshot-service.git
   cd screenshot-service

2. Build and start the services:
   ```bash
   docker-compose up --build

### Without docker

To run the project without Docker, ensure you have Python 3.11+ installed.

1. Clone the repository (you did it also in the previous step)
2. Create and activate a virtual environment:
    ```bash
        python3 -m venv venv
        source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. Install the dependencies
    ```bash
        pip install -r requirements.txt
    ```
4. Setup MongoDB
5. Setup the redis server
6. Set up MongoDB
   ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
7. The application should now be running at http://localhost:8000.

## Usage

### API endpoints

Once the application is running, you can access the API documentation at http://localhost:8000/docs.


## Testing

To run unit and integration tests, use:

```bash
pytest
```

## Monitoring

The project includes a monitoring setup with Prometheus. After starting the services with Docker Compose, access Prometheus at `http://localhost:9090`





