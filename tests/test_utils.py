from django.http import HttpRequest

from google_optimize.utils import _parse_experiments, get_experiments_variants


def test_parses_single_experiment_cookie():
    request = HttpRequest()
    request.COOKIES["_gaexp"] = "GAX1.2.utSuKi3PRbmxeG08en8VNw.18147.1"
    experiments = _parse_experiments(request)
    assert experiments == dict(utSuKi3PRbmxeG08en8VNw="1")


def test_parses_multiple_experiment_cookies():
    request = HttpRequest()
    request.COOKIES[
        "_gaexp"
    ] = "GAX1.2.3x8_BbSCREyqtWm1H1OUrQ.18166.1!7IXTpXmLRzKwfU-Eilh_0Q.18166.0"
    experiments = _parse_experiments(request)
    assert experiments == {"7IXTpXmLRzKwfU-Eilh_0Q": "0", "3x8_BbSCREyqtWm1H1OUrQ": "1"}


def test_parses_single_experiment():
    request = HttpRequest()
    request.COOKIES["_gaexp"] = "GAX1.2.utSuKi3PRbmxeG08en8VNw.18147.1"
    experiments = [
        {
            "id": "utSuKi3PRbmxeG08en8VNw",
            "alias": "redesign",
            "variant_aliases": ["old_design", "new_design"],
        }
    ]
    values = get_experiments_variants(request, experiments)
    assert values == {"redesign": "new_design"}


def test_parses_multiple_experiments():
    request = HttpRequest()
    request.COOKIES[
        "_gaexp"
    ] = "GAX1.2.3x8_BbSCREyqtWm1H1OUrQ.18166.1!7IXTpXmLRzKwfU-Eilh_0Q.18166.0"
    experiments = [
        {
            "id": "3x8_BbSCREyqtWm1H1OUrQ",
            "alias": "redesign_page",
            "variant_aliases": ["old_design", "new_design"],
        },
        {
            "id": "7IXTpXmLRzKwfU-Eilh_0Q",
            "alias": "resign_header",
            "variant_aliases": ["old_header", "new_header"],
        },
    ]
    values = get_experiments_variants(request, experiments)

    assert values == {"redesign_page": "new_design", "resign_header": "old_header"}


def test_parses_experiments_without_variant_aliases():
    request = HttpRequest()
    request.COOKIES["_gaexp"] = "GAX1.2.utSuKi3PRbmxeG08en8VNw.18147.1"
    experiments = [{"id": "utSuKi3PRbmxeG08en8VNw", "alias": "redesign"}]
    values = get_experiments_variants(request, experiments)
    assert values == {"redesign": "1"}


def test_parses_experiments_without_experiment_alias():
    request = HttpRequest()
    request.COOKIES["_gaexp"] = "GAX1.2.utSuKi3PRbmxeG08en8VNw.18147.1"
    experiments = [{"id": "utSuKi3PRbmxeG08en8VNw"}]
    values = get_experiments_variants(request, experiments)
    assert values == {"utSuKi3PRbmxeG08en8VNw": "1"}
