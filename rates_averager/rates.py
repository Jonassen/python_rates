from datetime import datetime, timedelta


class rates_averager:
    def __init__(self, repository):
        self.repository = repository

    def __resolve_location(self, location):
        if _is_port_code(location):
            return [location]

        return self.repository.resolve_regions(location)

    def computeRates(self, date_from, date_to, origin, destination):
        origins = self.__resolve_location(origin)
        destinations = self.__resolve_location(destination)

        data = self.repository.get_rates(
            date_from, date_to, origins, destinations)
        return _average_over_days(data, _build_dates(date_from, date_to))


def _parse_day(day):
    return datetime.strptime(day, "%Y-%m-%d")


def _build_dates(date_from, date_to):
    datetime_from = _parse_day(date_from)
    datetime_to = _parse_day(date_to)
    num_days = (datetime_to - datetime_from).days
    return [datetime_from + timedelta(days=x) for x in range(0, num_days + 1)]


# This seems sufficient to detect port codes from the example data
def _is_port_code(location):
    return len(location) == 5 and location.isupper()


def _average_list(rates):
    sums = {"sum": 0, "counts": 0}
    for rate in rates:
        sums["sum"] += rate["price"]
        sums["counts"] += 1

    if sums["counts"] < 3:
        return None
    return sums["sum"] / sums["counts"]


def _average_over_days(data, days):
    grouped_by_day = {}
    # Opted not to use a lib for the group by as the need is quite small
    for item in data:
        # Normalize date to remove time of day
        dt_object = item['day']
        key = datetime(dt_object.year, dt_object.month, dt_object.day)

        if key not in grouped_by_day:
            grouped_by_day[key] = []

        grouped_by_day[key].append(item)

    average_rates = []
    for day in days:
        average = None if day not in grouped_by_day else _average_list(
            grouped_by_day[day])
        average_rates.append({"day": day, "average": average})

    return average_rates
