from django.db import models


class GoogleExperiment(models.Model):
    experiment_id = models.CharField(max_length=50, unique=True)
    experiment_alias = models.CharField(
        max_length=30, unique=True, blank=True, null=True
    )
    active = models.BooleanField()


class ExperimentVariant(models.Model):
    index = models.IntegerField()
    alias = models.CharField(max_length=50)
    experiment_variant = models.ForeignKey(
        GoogleExperiment, null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["alias", "experiment_variant"],
                name="Can not have the same alias within an experiment_variant",
            ),
            models.UniqueConstraint(
                fields=["index", "experiment_variant"],
                name="Can not have the same index within an experiment_variant",
            ),
        ]
