extensions = ["sphinx.ext.intersphinx"]

master_doc = "index"

project = "django-google-optimize"
copyright = "Adin Hodovic and individual contributors."

# The short X.Y version.
version = "0.1"
# The full version, including alpha/beta/rc tags.
release = "0.1.3"

intersphinx_mapping = {
    "django": (
        "https://docs.djangoproject.com/en/stable",
        "https://docs.djangoproject.com/en/stable/_objects/",
    ),
    "python": ("https://docs.python.org/3", None),
}
