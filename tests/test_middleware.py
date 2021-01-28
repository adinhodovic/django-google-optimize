import pytest

from django_google_optimize.middleware import override_google_optimize

from .test_helpers import ExperimentVariantFactory, GoogleExperimentFactory

pytestmark = pytest.mark.django_db


def test_request_middleware(client):
    exp = GoogleExperimentFactory(experiment_alias="redesign")
    variant = ExperimentVariantFactory(index=1, alias="new_design", experiment=exp)
    client.cookies["_gaexp"] = f"GAX1.2.{exp.experiment_id}.18147.1"
    response = client.get("/test")
    assert response.wsgi_request.google_optimize == {
        exp.experiment_alias: variant.alias
    }


def test_template_middleware(client):
    exp = GoogleExperimentFactory(experiment_alias="redesign")
    ExperimentVariantFactory(index=1, alias="new_design", experiment=exp)
    client.cookies["_gaexp"] = f"GAX1.2.{exp.experiment_id}.18147.1"
    response = client.get("/test")
    assert response.content == b"new_design\n"


def test_override_google_optimize(client):
    experiments = {"my_experiment": "some_value"}
    with override_google_optimize(experiments):
        response = client.get("/test")
        assert response.context["request"].google_optimize == experiments
