# Rates averager

# Service dependencies

Rates averager requires a PostgreSQL instance version >= 12
Connection defined through environmentvariables `RATES_SERVER_DB_URL`, `RATES_SERVER_DB_USER`, and `RATES_SERVER_DB_PW`.

## Provided instance
An instance is provided through a dockerfile.
To run:
1. `docker build -t ratestask .`
2. `docker run -p 5432:5432 ratestask`

This instance is used by default through `./.env`s configuration file

# Setup

## Dependencies
This project requires a python venv to run (https://docs.python.org/3/library/venv.html)
To initiate a new venv run `python3 -m venv .venv`, to set the venv as active run `source .venv/bin/activate`
To install dependencies run `pip install -r requirements.txt`

## Running
To start the service run `flask --app main run`

# Spec
This service exposes one endpoint: `/rates` see main.py parameters and information

# tests
To run all tests run `pytest`

Integration tests require a running database to complete. To skip integration tests run `RATES_SERVER_SKIP_INTEGRATION=True pytest`

