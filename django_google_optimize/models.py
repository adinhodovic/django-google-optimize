from django.db import models


class GoogleExperiment(models.Model):
    experiment_id = models.CharField(max_length=50, unique=True)
    experiment_alias = models.CharField(
        max_length=30, unique=True, blank=True, null=True
    )
    active = models.BooleanField()


class ExperimentVariant(models.Model):
    index = models.IntegerField()
    alias = models.CharField(max_length=50, default="")
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


class ExperimentCookie(models.Model):
    active_variant_index = models.IntegerField(
        # pylint: disable=line-too-long
        help_text="Overrides or adds the cookie and sets the active variant for this experiment\nNOTE: ONLY WORKS IN DEBUG MODE"
    )
    active = models.BooleanField()
    experiment = models.OneToOneField(
        GoogleExperiment,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="experiment_cookie",
    )
