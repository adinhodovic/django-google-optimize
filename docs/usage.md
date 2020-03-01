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

## Forcing a specific experiment variant in tests

If you want to test a specific feature you are A/B testing you can force a
specific variant during the request lifecycle. You can use the context manager
`override_google_optimize()` to modify the context of the request in tests.

```python
from django_google_optimize.middleware import override_google_optimize

# As a context manager
def test_feature_a(client):
    with override_google_optimize({"feature_a": "true"}):
        response = client.get("/my-view")
        assert response.context["request"].google_optimize == {"feature_a": "true"}

# As a decorator
@override_google_optimize({"feature_a": "true"})
def test_feature_a_decorator(client):
    response = client.get("/my-view")
    assert response.context["request"].google_optimize == {"feature_a": "true"}
```
