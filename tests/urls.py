from django.urls import path

from tests.views import test

urlpatterns = [
    path("test", test, name="test"),
]
