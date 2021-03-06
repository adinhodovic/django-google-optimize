import factory

from django_google_optimize.models import (
    ExperimentCookie,
    ExperimentVariant,
    GoogleExperiment,
)


# pylint: disable=too-few-public-methods
class GoogleExperimentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoogleExperiment

    experiment_id = factory.Faker("sha1")
    experiment_alias = factory.Faker("city")
    active = True


# pylint: disable=too-few-public-methods
class ExperimentVariantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExperimentVariant

    alias = factory.Faker("city")
    index = factory.Faker("pyint")
    experiment = factory.SubFactory(GoogleExperimentFactory)


class ExperimentCookieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExperimentCookie

    active_variant_index = factory.Faker("pyint")
    active = True
    experiment = factory.SubFactory(GoogleExperimentFactory)
