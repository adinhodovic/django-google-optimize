from django.http import HttpRequest

from django_google_optimize.context_processors import google_experiment


def test_experiment_processor():
    request = HttpRequest()
    request.COOKIES["_gaexp"] = "GAX1.2.utSuKi3PRbmxeG08en8VNw.18147.1"
    experiment = google_experiment(request)
    assert experiment == dict(google_optimize={"redesign": "new_design"})


def test_context_processor_template(client):
    client.cookies["_gaexp"] = "GAX1.2.utSuKi3PRbmxeG08en8VNw.18147.1"
    response = client.get("/test")
    assert response.context["google_optimize"] == {"redesign": "new_design"}
