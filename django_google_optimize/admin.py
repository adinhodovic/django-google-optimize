from django.contrib import admin

from .models import ExperimentVariant, GoogleExperiment


class ExperimentVariantInline(admin.StackedInline):
    model = ExperimentVariant


@admin.register(GoogleExperiment)
class GoogleExperimentAdmin(admin.ModelAdmin):
    list_display = (
        "experiment_id",
        "experiment_alias",
    )
    inlines = [
        ExperimentVariantInline,
    ]
