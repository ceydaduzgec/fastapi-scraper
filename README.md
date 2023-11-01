# About Scrapper

This project is a web scraping application that allows you to extract data from websites.
FastAPI, Docker and PostgreSQL are used in this project.
It is designed to be easy to use and flexible, making it a powerful tool for collecting information from various sources.

## Pre-requisites

- Docker
- Docker Compose

## Installation

To get started with the project, follow these installation steps:

1. Clone the repository and navigate to the project directory:

   ```bash
   https://github.com/ceydaduzgec/fastapi-scraper.git```

2. Go to the project directory:

   ```bash
   cd project```

3. Run the following command to build and run the project with Docker:

   ```bash
   docker compose up --build```

4. (Optional) Create `.env` under `project` folder to store environment variables.

    ```bash
    DATABASE_URL=postgresql+psycopg2://user:password@db:5432/db_name
    DB_USER=user
    DB_PASSWORD=password
    DB_NAME=db_name
    PGADMIN_EMAIL=admin@admin.com
    PGADMIN_PASSWORD=admin_password
    DEBUG = True
    DOWNLOAD_PATH = downloads
    ```


## Virtual Environment

To create and install the dependincies in a virtual environment, run the following commands in the shell:

```bash
python3.11 -m venv env
source env/bin/activate
pip install -r app/requirements.txt
```

[More about it](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)

## Pre-commit Linting

Currently, project has `isort, black, flake8` for linting.
`isort` and `pre-commit` are working differently, need further investigation.

Install pre-commit:
`pip install pre-commit`

Install pre-commit hooks:
`pre-commit install`

Usage:
`pre-commit run --all-files`

## Tests and Coverage

To run the tests and see the coverage:
`python -m unittest discover app/tests`

To install coverage, first activate the docker and then run in the bash shell:
`pip install coverage`

Run the tests in the directory of `app/tests`:
`coverage run -m unittest discover app/tests`

Generate the coverage report html:
`coverage html`

Open the html:
`open htmlcov/index.html`

For further information about the details of the project:

- [Project Description](project_description.md)
- [Notes](notes.md)