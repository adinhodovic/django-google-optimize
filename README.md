# Django-google-optimize

![Lint](https://github.com/adinhodovic/django-google-optimize/workflows/Test/badge.svg)
![Test](https://github.com/adinhodovic/django-google-optimize/workflows/Lint/badge.svg)
[![Coverage](https://codecov.io/gh/adinhodovic/django-google-optimize/branch/master/graphs/badge.svg)](https://codecov.io/gh/adinhodovic/django-google-optimize/branch/master)
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
    "django_google_optimize",
    ...
]
```

Add the middleware:

```py
MIDDLEWARE = [
    ...
    "django_google_optimize.middleware.google_optimize",
    ...
]
```

## Getting started

Add settings for the experiments:

- id: Experiment ID required to identify variants for the experiment in templates
- alias: Alias for the experiment ID, optional useful for clarity in templates when accessing experiment variants by key
- variant_aliases: Aliases for each variant, each index represents a Optmize Experiment variant

```py
# django-google-optimize
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
{% if request.google_optimize.redesign == "new_design" %}
{% include "jobs/jobposting_list_new.html" %}
{% else %}
{% include "jobs/jobposting_list_old.html" %}
{% endif %}
```

Or use it inline:

```django
<nav class="navbar navbar-expand-lg navbar-dark
{% if request.google_optimize.redesign == "new_design" %} navbar-redesign{% endif %}">
```

Full documentation [can be found here.](https://django-google-optimize.readthedocs.io/en/latest/)

## Documentation and Support

More documentation can be found in the docs directory or read [online](https://django-google-optimize.readthedocs.io/en/latest/). Open a Github issue for support.
