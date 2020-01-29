from os import path

SECRET_KEY = "very-secret"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}}

INSTALLED_APPS = [
    "django_google_optimize",
]

MIDDLEWARE = [
    "django_google_optimize.middleware.google_optimize",
]

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

ROOT_URLCONF = "tests.urls"
