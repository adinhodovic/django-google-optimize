# Installing django-google-optimize

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

If you want to access the request in your templates remember to add the request context processor:

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [path.join(path.dirname(__file__), "templates"),],
        "OPTIONS": {
            "context_processors": ["django.template.context_processors.request",]
        },
    }
]
```
