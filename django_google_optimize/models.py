from django.db import models


class GoogleExperiment(models.Model):
    experiment_id = models.CharField(max_length=50, unique=True)
    experiment_alias = models.CharField(
        max_length=30, unique=True, blank=True, null=True, required=False
    )
    active = models.BooleanField()


class ExperimentVariant(models.Model):
    index = models.IntegerField()
    alias = models.CharField(max_length=50, blank=False, null=True, required=False)
    experiment = models.ForeignKey(
        GoogleExperiment,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="experiment_variant",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["alias", "experiment"],
                name="Can not have the same alias within an experiment_variant",
            ),
            models.UniqueConstraint(
                fields=["index", "experiment"],
                name="Can not have the same index within an experiment_variant",
            ),
        ]
