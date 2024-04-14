from .rates import _average_list, _is_port_code, _average_over_days, _build_dates, _parse_day
from datetime import datetime


def mock_prices(prices):
    return [{'price': price, 'day': _parse_day('2016-01-01')} for price in prices]


def test_calculates_simple_avarages_correctly():
    rates = mock_prices([100, 200, 600])
    average = _average_list(rates)
    assert average == 300

    assert 300 == _average_list(mock_prices([300, 300, 300, 300]))


def test_is_port_code_detects_known_codes():
    assert _is_port_code('baltic') is False
    assert _is_port_code('china_main') is False
    assert _is_port_code('north_europe_sub') is False
    assert _is_port_code('CNGGZ') is True
    assert _is_port_code('EETLL') is True


def test_average_correctly_collects_days():
    first_rates = mock_prices([100, 200, 300])
    second_rates = [{"price": item['price'], 'day': _parse_day('2016-01-02')}
                    for item in mock_prices([300, 400, 500])]
    multi_date_rates = _average_over_days(
        first_rates + second_rates, _build_dates("2016-01-01", "2016-01-02"))
    assert len(multi_date_rates) == 2


def test_returns_None_for_not_enough_data():
    rates = mock_prices([100, 200])
    average = _average_list(rates)
    assert average is None


def test_date_range_generator():
    dates = _build_dates("2016-01-01", "2016-01-05")
    assert datetime(2016, 1, 1) in dates
    assert datetime(2016, 1, 2) in dates
    assert datetime(2016, 1, 3) in dates
    assert datetime(2016, 1, 4) in dates
    assert datetime(2016, 1, 5) in dates


def test_datetime_parser():
    assert datetime(2016, 1, 1) == _parse_day('2016-01-01')
