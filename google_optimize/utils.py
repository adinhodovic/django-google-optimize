import logging

logger = logging.getLogger()


def get_experiments_variants(request, experiments):
    if not experiments:
        logger.error("Setting GOOGLE_OPTIMIZE_EXPERIMENTS not defined")
        return None

    try:
        experiment_variants = _parse_experiments(request)
    except Exception:  # pylint: disable=broad-except
        logger.error("Failed to parse _gaexp %s", request.COOKIES.get("_gaexp"))
        return None

    if not experiment_variants:
        logger.debug("Missing _ga_exp cookie")
        return None

    active_experiments = {}

    for experiment in experiments:

        experiment_id = experiment.get("id", None)
        experiment_alias = experiment.get("alias", None)
        variant_aliases = experiment.get("variant_aliases", None)

        if not experiment_id:
            logger.warning("experiment id not found in experiment settings")
            return None

        if experiment_id not in experiment_variants:
            logger.warning(
                "experiment id %s not found in experiments cookie %s",
                experiment_id,
                request.COOKIES["_gaexp"],
            )
            return None

        variant = experiment_variants[experiment_id]

        if variant_aliases:
            if variant in variant_aliases:
                variant = variant_aliases[variant]

        if experiment_alias:
            active_experiments[experiment_alias] = variant
        else:
            active_experiments[experiment_id] = variant

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
