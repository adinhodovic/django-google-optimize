from django.conf import settings

from .utils import _get_variant_value


def google_experiment(request):
    experiments = settings.GOOGLE_OPTIMIZE_EXPERIMENTS
    experiments_variants = _get_variant_value(request, experiments)
    return {"google_optimize": experiments_variants}
