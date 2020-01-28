import logging

from .models import GoogleExperiment

logger = logging.getLogger()


# pylint: disable=too-many-return-statements
def get_experiments_variants(request):
    experiments = GoogleExperiment.objects.all()
    if not experiments:
        logger.warning("No experiment added")
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

        experiment_variants = experiment.experiment_variant.all()

        if experiment_variants:
            variant = experiment_variants.filter(index=variant_name).first()
            if variant:
                if variant.alias:
                    variant_name = variant.alias
            else:
                logger.warning(
                    "No experiment variant added with the index %s", variant_name
                )
                return None
        else:
            logger.warning("No variants added")
            return None

        experiment_alias = experiment.experiment_alias
        if experiment_alias:
            active_experiments[experiment_alias] = variant_name
        else:
            active_experiments[experiment_id] = variant_name

    return active_experiments


def _parse_experiments(request):
    ga_exp = request.COOKIES.get("_gaexp")
    if not ga_exp:
        return None

    experiment_variations = {}

    parts = ga_exp.split(".")
    experiments_part = ".".join(parts[2:])
    experiments = experiments_part.split("!")
    for experiment_str in experiments:
        experiment_parts = experiment_str.split(".")
        experiment_id = experiment_parts[0]
        variation_id = int(experiment_parts[2])
        experiment_variations[experiment_id] = variation_id
    return experiment_variations
