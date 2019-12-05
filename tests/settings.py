INSTALLED_APPS = [
    "google_optimize",
    "tests",
]

SECRET_KEY = "very-secret"


GOOGLE_OPTIMIZE_EXPERIMENTS = [
    {
        "id": "utSuKi3PRbmxeG08en8VNw",
        "alias": "redesign",
        "variant_aliases": ["old_design", "new_design"],
    }
]
