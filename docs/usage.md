# Usage

## Usage in templates

Including various Django templates based on the experiment variant:

`jobs/xyz.html`

```django
{% if request.google_optimize.redesign == "new_design" %}
{% include "jobs/xyz_new.html" %}
{% else %}
{% include "jobs/xyz_old.html" %}
{% endif %}
```

Or you can use `django-google-optimize` inline:

```django
<nav class="navbar navbar-expand-lg navbar-dark
{% if request.google_optimize.redesign == "new_design" %}navbar-redesign{% endif %}
">
```

## Usage in views

To display two different templates based on the experiment variant:

```python
def get_template_names(self):
    variant = request.google_optimize.get("redesign", None)
    if variant == "new":
        return ["jobs/xyz_new.html"]
    return ["jobs/xyz_old.html"]
```

Adjust the queryset based on the experiment variant:

```python
def get_queryset(self):
    variant = self.request.google_optimize.get("redesign", None)

    if variant == "new":
        qs = qs.exclude(design__contains="old")
```
