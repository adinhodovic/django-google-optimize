from django.conf import settings

from .utils import get_experiments_variants


def google_experiment(request):

    experiments = getattr(settings, "GOOGLE_OPTIMIZE_EXPERIMENTS", None)

    experiments_variants = get_experiments_variants(request, experiments)
    return {"google_optimize": experiments_variants}
