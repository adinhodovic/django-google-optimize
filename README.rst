# Django-google-optimize

[![Build status](https://gitlab.com/hodovicadin/django-google-optimize/badges/master/pipeline.svg)](https://gitlab.com/hodovicadin/django-google-optimize/commits/master)
[![Coverage](https://gitlab.com/hodovicadin/django-google-optimize/badges/master/coverage.svg)](https://gitlab.com/hodovicadin/django-google-optimize/commits/master)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/django-google-optimize.svg)](https://pypi.org/project/django-google-optimize/)
[![PyPI Version](https://img.shields.io/pypi/v/django-google-optimize.svg?style=flat)](https://pypi.org/project/django-google-optimize/)

Django-google-optimize is a reusable Django application designed to make running server side Google Optimize A/B test easy.

## Installation

Install django-google-optimize with pip:

`pip install django-google-optimize`

Add the application to installed django applications:

```py
DJANGO_APPS = [
    ...
    "google_optimize",
    ...
]
```

Add the context processor:

```py
"context_processors": [
    ...
    "google_optimize.context_processors.google_experiment",
    ...
]
```

## Getting started

Add settings for the experiments:

- id: Experiment ID required to identify variants for the experiment in templates
- alias: Alias for the experiment ID, optional useful for clarity in templates when accessing experiment variants by key
- variant_aliases: Aliases for each variant, each index represents a Optmize Experiment variant

```py
# google-optimize
GOOGLE_OPTIMIZE_EXPERIMENTS = [
    {
        "id": "utSuKi3PRbmxeG08en8VNw",
        "alias": "redesign",
        "variant_aliases": {0: "old_design", 1: "new_design"},
    }
]
```

Now you can access the experiment in templates:

```django
{% if google_optimize.redesign == "new_design" %}
{% include "jobs/jobposting_list_new.html" %}
{% else %}
{% include "jobs/jobposting_list_old.html" %}
{% endif %}
```

Or use it inline:

```django
<nav class="navbar navbar-expand-lg navbar-dark
{% if google_optimize.redesign == "new_design" %} navbar-redesign{% endif %}">
```

Full documentation [can be found here.](https://django-google-optimize.readthedocs.io/en/latest/)

## Documentation and Support

More documentation can be found in the docs directory or read [online](https://django-google-optimize.readthedocs.io/en/latest/). Open a Github issue for support.
