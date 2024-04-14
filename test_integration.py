import pytest
import os
from main import create_app


@pytest.fixture()
def app():
    app = create_app()

    yield app


@pytest.mark.skipif(os.environ.get("RATES_SERVER_SKIP_INTEGRATION"), reason="skip flag set")
def test_returns_404_unknown_path(app):
    tc = app.test_client()
    res = tc.get("invalid_path")

    assert res.status_code == 404


@pytest.mark.skipif(os.environ.get("RATES_SERVER_SKIP_INTEGRATION"), reason="skip flag set")
def test_returns_default_green_path(app):
    tc = app.test_client()
    res = tc.get("rates?date_to=2016-01-22&date_from=2016-01-15&origin=china_main&destination=baltic")

    assert res.status_code == 200
