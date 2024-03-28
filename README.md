# Blog Application

This repository contains the code for a Blog application built with Django and Django REST Framework. It utilizes Docker for containerization and GitHub Actions for continuous integration.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Docker and Docker Compose are installed on your machine.
- Basic knowledge of Docker, Django, and Django REST Framework.

## Setup and Running with Docker

### Building the Docker Image

To build the Docker images for the application and its services, run the following command from the root of the project:

```bash
docker-compose build
```
### Starting the Containers

```bash
docker-compose up
```

### Creating Database Migrations
```bash
docker-compose run web python manage.py makemigrations
```
### Applying Database Migrations
```bash
docker-compose run web python manage.py migrate
```
### Creating a Superuser
```bash
docker-compose run web python manage.py createsuperuser
```
### Accessing the Application

The web application at http://localhost:8000

### Running Tests
```bash
docker-compose run web python manage.py test
```
### Continuous Integration with GitHub Actions

This project is configured to use GitHub Actions for continuous integration. Upon each push or pull request, GitHub Actions will:

Build the Docker image.
Run tests within the Docker environment.
Perform any additional steps defined in .github/workflows/django.yml.
You can view the results of these actions in the "Actions" tab of the GitHub repository.


### Contributing

Contributions to this project are welcome. Please ensure you follow the established patterns, and feel free to submit pull requests or create issues for bugs and feature requests.

