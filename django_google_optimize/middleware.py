from contextlib import ContextDecorator

from .utils import get_experiments_variants


def google_optimize(get_response):
    def middleware(request):
        request.google_optimize = get_experiments_variants(request) or {}
        return get_response(request)

    return middleware


class override_google_optimize(ContextDecorator):
    def __init__(self, experiments=None):
        self.experiments = experiments
        self.original_fn = get_experiments_variants

    def __enter__(self):
        global get_experiments_variants  # pylint: disable=global-statement
        get_experiments_variants = lambda _: self.experiments

    def __exit__(self, exc_type, exc, exc_tb):
        global get_experiments_variants  # pylint: disable=global-statement
        get_experiments_variants = self.original_fn
