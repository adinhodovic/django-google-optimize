# Configuration

You can configure the Google Optimize experiments via the Django admin panel. There are three objects that you can add:

- Google Experiment.
- Experiment Variant
- Experiment Cookie

The Google Experiment object contains of an experiment id and an optional alias which can used to alternatively reference the experiment by the alias in code.

The Experiment Variant is optional and it is used to give each experiment variant an alias for easier usage in templates/views. If not added, the returned variant will be the index of the variant in the Google Optimize experiment cookie(_gaexp).

The Experiment Cookie is optional and it is only used in DEBUG mode. It aids in overriding or adding an experiment to the browser cookie(_gaexp). Replaces any interaction with the browser session while developing, making it possible to test out all your variants via the Django-admin.

## Samples of usage with and without aliases

Without an Google Experiment alias you will have to reference your experiment by id:

```python
    {% if request.google_optimize.k123ladwq == 0 %}
    {% include "jobs/xyz_new.html" %}
    {% endif %}
```

Instead of by experiment alias:

```python
    {% if request.google_optimize.redesign_header == 0 %}
    {% include "jobs/xyz_new.html" %}
    {% endif %}
```

Without an variant alias you will have to reference your variant by index as:

```python
    {% if request.google_optimize.redesign_header == 0 %}
    {% include "jobs/xyz_new.html" %}
    {% endif %}
```

Instead of by variant alias:

```python
    {% if request.google_optimize.redesign_header == "New Background Color" %}
    {% include "jobs/xyz_new.html" %}
    {% endif %}
```

If you do not use the Experiment Cookie object when testing locally make sure to add the `_gaexp` cookie to the session:

```txt
Cookie Name: _gaexp
Cookie Value GAX1.2.{experiment_id}.18147.{active_variant_index}
```
