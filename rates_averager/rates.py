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
        return _average_over_days(data)


# This seems sufficient to detect port codes from the example data
def _is_port_code(location):
    return len(location) == 5 and location.isupper()


def _average_list(rates):
    sums = {"sum": 0, "counts": 0}
    for rate in rates:
        sums["sum"] += rate["price"]
        sums["counts"] += 1
    return sums["sum"] / sums["counts"]


def _average_over_days(data):
    grouped_by_day = {}
    # Opted not to use a lib for the group by as the need is quite small
    for item in data:
        key = item['day']

        if key not in grouped_by_day:
            grouped_by_day[key] = []

        grouped_by_day[key].append(item)

    average_rates = []
    # for day, values in groupby(data, key=lambda item: item['day']):
    for day, values in grouped_by_day.items():
        average = _average_list(values)
        average_rates.append({"day": day, "average": average})

    return average_rates
