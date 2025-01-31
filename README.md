### Hexlet tests and linter status:
[![Actions Status](https://github.com/putilovms/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/putilovms/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/e87e34c3fc14175c24b3/maintainability)](https://codeclimate.com/github/putilovms/python-project-83/maintainability)

# Page Analyzer
*Educational project*

A service that checks the presence of the main elements of SEO optimization on the monitored site and their content.

Link to the project's website: [https://page-analyzer-uiqi.onrender.com](https://page-analyzer-uiqi.onrender.com)

***Notice**: the project uses a free hosting plan, the request can take up to 50 seconds.*

## System requirements:

* Python 3.10 or higher
* PostgreSQL database

## Installation

1. Requires Python version 3.10 or higher and Poetry
2. Clone the project: `>> git clone git@github.com:putilovms/page-analyzer.git`
3. Create an `.env` file in the root of the project and add the following variables to it:
    * `SECRET_KEY` - the secret key
    * `DATABASE_URL` - access to the PostgreSQL database
4. Build the project using the command: `>> make build`
5. Starting the server: `>> make start`

## Docker Compose

1. Create files for environment variables with the following contents:
   * `/compose/env/postgres.env`
      * `POSTGRES_DB` - database name
      * `POSTGRES_USER` - username
      * `POSTGRES_PASSWORD` - password
   * `/compose/env/page_analyzer.env`
      * `SECRET_KEY` - the secret key
      * `DATABASE_URL` - access to the PostgreSQL database
2. The command to launch containers `>> docker-compose up --build`
