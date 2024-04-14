from .rates import _average_list, _is_port_code, _average_over_days


def mock_prices(prices):
    return [{'price': price, 'day': '2016-01-01'} for price in prices]


def test_calculates_simple_avarages_correctly():
    rates = mock_prices([100, 200])
    average = _average_list(rates)
    assert average == 150

    assert 300 == _average_list(mock_prices([300, 300, 300, 300]))


def test_is_port_code_detects_known_codes():
    assert _is_port_code('baltic') is False
    assert _is_port_code('china_main') is False
    assert _is_port_code('north_europe_sub') is False
    assert _is_port_code('CNGGZ') is True
    assert _is_port_code('EETLL') is True


def test_average_correctly_collects_days():
    jan_rates = mock_prices([100, 200])
    feb_rates = [{"price": item['price'], 'day': '2016-02-01'}
                 for item in mock_prices([300, 400])]
    multi_date_rates = _average_over_days(jan_rates + feb_rates)
    assert len(multi_date_rates) == 2
