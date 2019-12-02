from django.http import HttpRequest

from .google_experiments import _parse_experiments


def test_parses_single_experiment():
    req = HttpRequest()
    req.COOKIES["_gaexp"] = "GAX1.2.utSuKi3PRbmxeG08en8VNw.18147.1"
    experiments = _parse_experiments(req)
    assert experiments == dict(utSuKi3PRbmxeG08en8VNw="1")


def test_parses_multiple_experiments():
    req = HttpRequest()
    req.COOKIES[
        "_gaexp"
    ] = "GAX1.2.3x8_BbSCREyqtWm1H1OUrQ.18166.1!7IXTpXmLRzKwfU-Eilh_0Q.18166.0"
    experiments = _parse_experiments(req)
    assert experiments == {"7IXTpXmLRzKwfU-Eilh_0Q": "0", "3x8_BbSCREyqtWm1H1OUrQ": "1"}
