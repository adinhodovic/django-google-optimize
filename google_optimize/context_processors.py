from django.conf import settings

from .utils import get_experiments_variants


def google_experiment(request):
    experiments = settings.GOOGLE_OPTIMIZE_EXPERIMENTS
    experiments_variants = get_experiments_variants(request, experiments)
    return {"google_optimize": experiments_variants}
