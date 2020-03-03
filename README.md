# Django-google-optimize

![Lint](https://github.com/adinhodovic/django-google-optimize/workflows/Test/badge.svg)
![Test](https://github.com/adinhodovic/django-google-optimize/workflows/Lint/badge.svg)
[![Coverage](https://codecov.io/gh/adinhodovic/django-google-optimize/branch/master/graphs/badge.svg)](https://codecov.io/gh/adinhodovic/django-google-optimize/branch/master)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/django-google-optimize.svg)](https://pypi.org/project/django-google-optimize/)
[![PyPI Version](https://img.shields.io/pypi/v/django-google-optimize.svg?style=flat)](https://pypi.org/project/django-google-optimize/)

Django-google-optimize is a Django application designed to make running Google Optimize A/B tests easy.

## Installation

Install django-google-optimize with pip:

`pip install django-google-optimize`

Add the application to installed Django applications:

```py
# settings.py
INSTALLED_APPS = [
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

Head over to the Django admin and add a new Google Optimize experiment. Add an experiment variant with the index 1 and the alias "new_design". Set the experiment cookie's active variant index to 1. Now the active variant index for that experiment is 1 which is the experiment variant with the alias "new_design" that you created.

Now you can access the experiment in templates by the experiment alias and the variant alias:

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

Note: The experiment cookie only works in DEBUG mode and is used to avoid interacting with the session to add the `_gaexp` cookie making it possible to test the experiment variants through the Django admin.

Full documentation [can be found here.](https://django-google-optimize.readthedocs.io/en/latest/)

## Documentation and Support

More documentation can be found in the docs directory or read [online](https://django-google-optimize.readthedocs.io/en/latest/). Open a Github issue for support.
