from unittest import mock

from django.http import HttpRequest

from google_optimize.utils import _parse_experiments, get_experiments_variants


def test_parses_single_experiment_cookie():
    request = HttpRequest()
    request.COOKIES["_gaexp"] = "GAX1.2.utSuKi3PRbmxeG08en8VNw.18147.1"
    experiments = _parse_experiments(request)
    assert experiments == dict(utSuKi3PRbmxeG08en8VNw=1)


def test_parses_multiple_experiment_cookies():
    request = HttpRequest()
    request.COOKIES[
        "_gaexp"
    ] = "GAX1.2.3x8_BbSCREyqtWm1H1OUrQ.18166.1!7IXTpXmLRzKwfU-Eilh_0Q.18166.0"
    experiments = _parse_experiments(request)
    assert experiments == {"7IXTpXmLRzKwfU-Eilh_0Q": 0, "3x8_BbSCREyqtWm1H1OUrQ": 1}


def test_parses_without_cookie():
    request = HttpRequest()
    experiments = _parse_experiments(request)
    assert experiments is None


@mock.patch("logging.Logger.debug")
def test_logs_missing_gaexp_cookie(logger):
    request = HttpRequest()
    get_experiments_variants(request, [{"id": "abc"}])
    logger.assert_called_with("Missing _ga_exp cookie")


@mock.patch("logging.Logger.error")
def test_logs_no_settings(logger):
    request = HttpRequest()
    request.COOKIES["_gaexp"] = "test"
    get_experiments_variants(request, None)
    logger.assert_called_with("Setting GOOGLE_OPTIMIZE_EXPERIMENTS not defined")


@mock.patch("logging.Logger.error")
def test_logs_failed_cookie_parsing(logger):
    request = HttpRequest()
    request.COOKIES["_gaexp"] = "test"
    get_experiments_variants(request, [{"id": "abc"}])
    logger.assert_called_with("Failed to parse _gaexp %s", "test")


@mock.patch("logging.Logger.warning")
def test_logs_settings_missing_experiment_id(logger):
    request = HttpRequest()
    request.COOKIES["_gaexp"] = "GAX1.2.3x8_BbSCREyqtWm1H1OUrQ.18166.1"
    get_experiments_variants(request, [{"test": "test"}])
    logger.assert_called_with("experiment id not found in experiment settings")


@mock.patch("logging.Logger.warning")
def test_logs_experiment_id_not_in_cookies(logger):
    request = HttpRequest()
    gaexp = "GAX1.2.3x8_BbSCREyqtWm1H1OUrQ.18166.1"
    experiment_id = "test"
    request.COOKIES["_gaexp"] = gaexp
    get_experiments_variants(request, [{"id": experiment_id}])
    logger.assert_called_with(
        "experiment id %s not found in experiments cookie %s", experiment_id, gaexp
    )


def test_parses_single_experiment():
    request = HttpRequest()
    request.COOKIES["_gaexp"] = "GAX1.2.utSuKi3PRbmxeG08en8VNw.18147.1"
    experiments = [
        {
            "id": "utSuKi3PRbmxeG08en8VNw",
            "alias": "redesign",
            "variant_aliases": {0: "old_design", 1: "new_design"},
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
            "variant_aliases": {0: "old_design", 1: "new_design"},
        },
        {
            "id": "7IXTpXmLRzKwfU-Eilh_0Q",
            "alias": "resign_header",
            "variant_aliases": {0: "old_header", 1: "new_header"},
        },
    ]
    values = get_experiments_variants(request, experiments)

    assert values == {"redesign_page": "new_design", "resign_header": "old_header"}


def test_parses_experiments_without_variant_aliases():
    request = HttpRequest()
    request.COOKIES["_gaexp"] = "GAX1.2.utSuKi3PRbmxeG08en8VNw.18147.1"
    experiments = [{"id": "utSuKi3PRbmxeG08en8VNw", "alias": "redesign"}]
    values = get_experiments_variants(request, experiments)
    assert values == {"redesign": 1}


def test_parses_experiments_without_experiment_alias():
    request = HttpRequest()
    request.COOKIES["_gaexp"] = "GAX1.2.utSuKi3PRbmxeG08en8VNw.18147.1"
    experiments = [{"id": "utSuKi3PRbmxeG08en8VNw"}]
    values = get_experiments_variants(request, experiments)
    assert values == {"utSuKi3PRbmxeG08en8VNw": 1}
