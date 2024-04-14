from main import validate_parameters


def test_requires_all_params():
    validation = validate_parameters(None, None, None, None)
    assert validation[0] is False
    assert len(validation[1]) == 4


def test_asserts_date_order():
    validation = validate_parameters(
        '2016-02-01', '2016-01-01', 'CNGGZ', 'EETTL')
    assert validation[0] is False
    assert validation[1][0] == 'date_to must be greater than date_from'


def test_validates_for_good_params():
    validation = validate_parameters(
        '2016-01-01', '2016-02-01', 'CNGGZ', 'EETTL')
    assert validation[0] is True
