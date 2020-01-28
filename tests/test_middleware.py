import pytest

from .test_helpers import ExperimentVariantFactory, GoogleExperimentFactory


@pytest.mark.django_db
def test_request_middleware(client):
    exp = GoogleExperimentFactory(experiment_alias="redesign")
    variant = ExperimentVariantFactory(index=1, alias="new_design", experiment=exp)
    client.cookies["_gaexp"] = f"GAX1.2.{exp.experiment_id}.18147.1"
    response = client.get("/test")
    assert response.wsgi_request.google_optimize == {
        exp.experiment_alias: variant.alias
    }


@pytest.mark.django_db
def test_template_middleware(client):
    exp = GoogleExperimentFactory(experiment_alias="redesign")
    ExperimentVariantFactory(index=1, alias="new_design", experiment=exp)
    client.cookies["_gaexp"] = f"GAX1.2.{exp.experiment_id}.18147.1"
    response = client.get("/test")
    assert response.content == b"new_design\n"
