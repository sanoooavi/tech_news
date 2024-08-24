![PostgreSQL Badge](https://img.shields.io/badge/PostgreSQL--%23336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Django Badge](https://img.shields.io/badge/Django--%23092E20?style=for-the-badge&logo=django&logoColor=white)
![Docker Badge](https://img.shields.io/badge/Docker--%232496ED?style=for-the-badge&logo=docker&logoColor=white)
![Static Badge](https://img.shields.io/badge/Celery--yellowgreen?style=for-the-badge&logo=celery&logoColor=white)

## Overview

This project is a web scraping application designed to collect tech news from [Zoomit.ir](https://www.zoomit.ir/) and serve it through a Django REST API. The project is divided into three main parts:

### 1. Django REST API

The Django REST API is the core of this project, responsible for providing endpoints to interact with the tech news data. The API supports the following functionalities:

- **Fetch All News**: Retrieves all news stored in the database.
- **Fetch News by Tags**: Allows filtering of news based on specific tags provided by the user.

The API is thoroughly tested to ensure all endpoints function as expected and handle edge cases gracefully.

### 2. Web Scraping

The second part of the project involves scraping tech news from [Zoomit.ir](https://www.zoomit.ir/). The scraper is built to run periodically, fetching the latest articles and storing them in the PostgreSQL database. This ensures that the database is always up-to-date with the latest tech news.

### 3. Celery Integration and Dockerization

To automate the scraping process, Celery and Celery Beat are used. These tools schedule and manage scraping tasks at regular intervals, ensuring continuous data collection without manual intervention.

Additionally, the entire project is Dockerized to streamline the development, testing, and deployment processes. Docker containers allow for consistent environments across different stages, from development to production.

The application is deployed and can be accessed at: [https://tech-news-zoomit.darkube.app/](https://tech-news-zoomit.darkube.app/).

## Getting Started

To get a local copy of this project up and running, follow these simple steps.

### Prerequisites

- **Docker**: Ensure you have Docker installed on your machine.
- **Docker Compose**: Required for orchestrating the multi-container Docker application.

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/tech-news-scraper.git
    cd tech-news-scraper
    ```

2. **Build and run the Docker containers**:
    ```bash
    docker-compose up --build
    ```

3. **Apply migrations and create a superuser**:
    ```bash
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    ```

4. **Run Celery**:
    ```bash
    docker-compose exec web celery -A yourprojectname worker -l info
    docker-compose exec web celery -A yourprojectname beat -l info
    ```

5. **Access the application**:
   - Open your browser and navigate to `http://localhost:8000` to access the Django REST API.
   - Admin interface: `http://localhost:8000/admin/`

### Usage

- **API Endpoints**:
  - `GET /api/news/` - Fetch all news.
  - `GET /api/news/?tags=<tag>` - Fetch news filtered by a specific tag.
