from django.conf import settings

from .utils import get_experiments_variants

experiments = getattr(settings, "GOOGLE_OPTIMIZE_EXPERIMENTS", None)


def google_optimize(get_response):
    def middleware(request):
        request.google_optimize = get_experiments_variants(request, experiments)
        return get_response(request)

    return middleware
