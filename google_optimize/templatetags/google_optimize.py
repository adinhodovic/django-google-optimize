from django import template

from google_optimize.utils import _get_variant_value

register = template.Library()


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
