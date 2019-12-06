from os import path

SECRET_KEY = "very-secret"

INSTALLED_APPS = [
    "google_optimize",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [path.join(path.dirname(__file__), "templates"),],
        "OPTIONS": {
            "context_processors": [
                "google_optimize.context_processors.google_experiment",
            ]
        },
    }
]

ROOT_URLCONF = "tests.urls"

GOOGLE_OPTIMIZE_EXPERIMENTS = [
    {
        "id": "utSuKi3PRbmxeG08en8VNw",
        "alias": "redesign",
        "variant_aliases": ["old_design", "new_design"],
    }
]
