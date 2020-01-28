from .utils import get_experiments_variants


def google_optimize(get_response):
    def middleware(request):
        request.google_optimize = get_experiments_variants(request)
        return get_response(request)

    return middleware
