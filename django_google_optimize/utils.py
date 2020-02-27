import logging

from django.conf import settings

from .models import ExperimentCookie, GoogleExperiment

logger = logging.getLogger()


# pylint: disable=too-many-return-statements
def get_experiments_variants(request):
    experiments = GoogleExperiment.objects.filter(active=True)
    if not experiments:
        return None

    try:
        cookie_data = _parse_experiments(request)
    except Exception:  # pylint: disable=broad-except
        logger.warning("Failed to parse _gaexp %s", request.COOKIES.get("_gaexp"))
        return None

    if not cookie_data:
        logger.debug("Missing _ga_exp cookie")
        return None

    active_experiments = {}

    for experiment in experiments:

        experiment_id = experiment.experiment_id

        if experiment_id not in cookie_data:
            logger.warning(
                "experiment id %s not found in experiments cookie %s",
                experiment_id,
                request.COOKIES["_gaexp"],
            )
            return None

        variant_name = cookie_data[experiment_id]

        variant = experiment.experiment_variant.all().filter(index=variant_name).first()
        if variant:
            variant_name = variant.alias

        if experiment.experiment_alias:
            active_experiments[experiment.experiment_alias] = variant_name
        else:
            active_experiments[experiment_id] = variant_name

    return active_experiments


def _parse_experiments(request,):
    ga_exp = request.COOKIES.get("_gaexp")

    experiment_variations = {}
    if ga_exp:
        parts = ga_exp.split(".")
        experiments_part = ".".join(parts[2:])
        experiments = experiments_part.split("!")
        for experiment_str in experiments:
            experiment_parts = experiment_str.split(".")
            experiment_id = experiment_parts[0]
            variation_id = int(experiment_parts[2])
            experiment_variations[experiment_id] = variation_id
    if settings.DEBUG:
        cookies = ExperimentCookie.objects.filter(active=True)
        for cookie in cookies:
            experiment_variations[
                cookie.experiment.experiment_id
            ] = cookie.active_variant_index
    if experiment_variations:
        return experiment_variations
    return None
