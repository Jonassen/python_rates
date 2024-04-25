from flask import Flask, request
from rates_averager.rates import rates_averager
from database.database import rates_repository
from datetime import datetime
from config import config
import json


def create_app():
    app = Flask(__name__)

    repo = rates_repository(config['db_connection_string'])
    rates_calculator = rates_averager(repo)

    # This endpoint requires all parameters set to function:
    # `date_to`: date formated yyyy-mm-dd
    # `date_from`: date formated yyyy-mm-dd
    # `destination`: portcode or shipping region
    # `origin`: portcode or shipping region

    @app.route("/rates")
    def get_rates():
        date_to = request.args.get('date_to')
        date_from = request.args.get('date_from')
        destination = request.args.get('destination')
        origin = request.args.get('origin')

        validation = validate_parameters(
            date_from, date_to, origin, destination)
        if not validation[0]:
            return json.dumps(validation[1]), 400

        average_rates = rates_calculator.computeRates(
            date_from, date_to, origin, destination)

        if len(average_rates) == 0:
            return "", 404

        return json.dumps(average_rates, default=str)

    return app


def validate_parameters(date_from, date_to, origin, destination):
    errors = []
    if date_to is None:
        errors.append("Missing required date_to parameter")
    if date_from is None:
        errors.append("Missing required date_from parameter")
    if origin is None:
        errors.append("Missing required origin parameter")
    if destination is None:
        errors.append("Missing required destination parameter")

    if (
            (date_to is not None)
            and (date_from is not None)
            and (datetime.fromisoformat(date_to) < datetime.fromisoformat(date_from))
    ):
        errors.append("date_to must be greater than date_from")

    if len(errors) == 0:
        return True, errors

    return False, errors
