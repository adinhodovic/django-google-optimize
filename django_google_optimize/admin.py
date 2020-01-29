from django.contrib import admin

from .models import ExperimentCookie, ExperimentVariant, GoogleExperiment


class ExperimentCookieInline(admin.StackedInline):
    model = ExperimentCookie


class ExperimentVariantInline(admin.StackedInline):
    model = ExperimentVariant


@admin.register(GoogleExperiment)
class GoogleExperimentAdmin(admin.ModelAdmin):
    list_display = (
        "experiment_id",
        "experiment_alias",
    )
    inlines = [ExperimentVariantInline, ExperimentCookieInline]
