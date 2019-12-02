import logging

logger = logging.LoggerAdapter(logging.getLogger(), extra={"app": "google_experiments"})


def _get_variant_value(request, experiment_id, variant_values):
    try:
        experiment_variants = _parse_experiments(request)
    except Exception:  # pylint: disable=broad-except
        logger.error(
            "Failed to parse _gaexp", extra=dict(_gaexp=request.COOKIES.get("_gaexp"))
        )
        return None

    if not experiment_variants:
        logger.warning("Missing _ga_exp cookie")
        return None

    if experiment_id not in experiment_variants:
        logger.warning(
            "experiment_id not found in experiments cookie",
            extra=dict(experiment_id=experiment_id, _gaexp=request.COOKIES["_gaexp"]),
        )
        return None

    variant = experiment_variants[experiment_id]
    if variant not in variant_values:
        logger.warning(
            "variant not found in source code experiment variants",
            extra=dict(variant=variant, variant_values=variant_values),
        )
        return None

    return variant_values[variant]


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
        variation_id = experiment_parts[2]
        experiment_variations[experiment_id] = variation_id
    return experiment_variations

@register.simple_tag(takes_context=True)
def google_experiment(context, **kwargs):
    experiment_id = kwargs["experiment_id"]
    original_variant = kwargs["original_variant"]
    experiment_values = kwargs["experiment_values"]
    variants = {}
    for index, experiment_value in enumerate(experiment_values.split(",")):
        variants[str(index)] = experiment_value
    value = _get_variant_value(context["request"], experiment_id, variants)
    return value or original_variant
