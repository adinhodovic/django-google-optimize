from unittest import mock

import pytest
from django.http import HttpRequest

from .test_helpers import ExperimentVariantFactory, GoogleExperimentFactory

from django_google_optimize.utils import _parse_experiments, get_experiments_variants


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


@pytest.mark.django_db
@mock.patch("logging.Logger.debug")
def test_logs_missing_gaexp_cookie(logger):
    GoogleExperimentFactory()

    request = HttpRequest()
    get_experiments_variants(request)
    logger.assert_called_with("Missing _ga_exp cookie")


@pytest.mark.django_db
@mock.patch("logging.Logger.warning")
def test_logs_no_settings(logger):
    request = HttpRequest()
    request.COOKIES["_gaexp"] = "test"
    get_experiments_variants(request)
    logger.assert_called_with("No experiment added")


@pytest.mark.django_db
@mock.patch("logging.Logger.warning")
def test_logs_failed_cookie_parsing(logger):
    GoogleExperimentFactory()
    request = HttpRequest()
    request.COOKIES["_gaexp"] = "test"
    get_experiments_variants(request)
    logger.assert_called_with("Failed to parse _gaexp %s", "test")


@pytest.mark.django_db
@mock.patch("logging.Logger.warning")
def test_logs_no_variants(logger):
    exp = GoogleExperimentFactory()
    request = HttpRequest()
    request.COOKIES["_gaexp"] = f"GAX1.2.{exp.experiment_id}.18147.1"
    get_experiments_variants(request)
    logger.assert_called_with("No variants added")


@pytest.mark.django_db
@mock.patch("logging.Logger.warning")
def test_logs_no_experiment_variant(logger):
    exp = GoogleExperimentFactory()
    ExperimentVariantFactory(index=0, alias="new_design", experiment=exp)
    request = HttpRequest()
    request.COOKIES["_gaexp"] = f"GAX1.2.{exp.experiment_id}.18147.1"
    get_experiments_variants(request)
    logger.assert_called_with("No experiment variant added with the index %s", 1)


@pytest.mark.django_db
@mock.patch("logging.Logger.warning")
def test_logs_experiment_id_not_in_cookies(logger):
    exp = GoogleExperimentFactory()
    request = HttpRequest()
    gaexp = f"GAX1.2.3x8_BbSCREyqtWm1H1OUrQ.18166.1"
    request.COOKIES["_gaexp"] = gaexp
    get_experiments_variants(request)
    logger.assert_called_with(
        "experiment id %s not found in experiments cookie %s", exp.experiment_id, gaexp
    )


@pytest.mark.django_db
def test_parses_single_experiment():
    exp = GoogleExperimentFactory()
    variant = ExperimentVariantFactory(index=1, alias="new_design", experiment=exp)
    request = HttpRequest()
    request.COOKIES["_gaexp"] = f"GAX1.2.{exp.experiment_id}.18147.1"
    values = get_experiments_variants(request)
    assert values == {exp.experiment_alias: variant.alias}


@pytest.mark.django_db
def test_parses_multiple_experiments():
    exp_1 = GoogleExperimentFactory()
    variant_1 = ExperimentVariantFactory(index=1, alias="new_design", experiment=exp_1)

    exp_2 = GoogleExperimentFactory()
    variant_2 = ExperimentVariantFactory(index=0, alias="new_header", experiment=exp_2)

    request = HttpRequest()
    request.COOKIES[
        "_gaexp"
    ] = f"GAX1.2.{exp_1.experiment_id}.18166.1!{exp_2.experiment_id}.18166.0"

    values = get_experiments_variants(request)

    assert values == {
        exp_1.experiment_alias: variant_1.alias,
        exp_2.experiment_alias: variant_2.alias,
    }


@pytest.mark.django_db
def test_parses_experiments_without_experiment_alias():
    exp = GoogleExperimentFactory(experiment_alias=None)
    variant = ExperimentVariantFactory(index=1, experiment=exp)
    request = HttpRequest()
    request.COOKIES["_gaexp"] = f"GAX1.2.{exp.experiment_id}.18147.1"
    values = get_experiments_variants(request)
    assert values == {exp.experiment_id: variant.alias}


@pytest.mark.django_db
def test_parses_experiments_without_variant_alias():
    exp = GoogleExperimentFactory()
    variant = ExperimentVariantFactory(index=1, alias=None, experiment=exp)
    request = HttpRequest()
    request.COOKIES["_gaexp"] = f"GAX1.2.{exp.experiment_id}.18147.{variant.index}"
    values = get_experiments_variants(request)
    assert values == {exp.experiment_alias: variant.index}


@pytest.mark.django_db
def test_filters_active_experiments():
    exp = GoogleExperimentFactory()
    GoogleExperimentFactory(active=False)
    variant = ExperimentVariantFactory(index=1, experiment=exp)
    request = HttpRequest()
    request.COOKIES["_gaexp"] = f"GAX1.2.{exp.experiment_id}.18147.{variant.index}"
    values = get_experiments_variants(request)
    assert values == {exp.experiment_alias: variant.alias}
