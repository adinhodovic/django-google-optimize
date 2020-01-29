# Configuration

You can configure the Google Optimize experiments via the Django admin panel. There are three objects that you can add:

- Google Experiment.
- Experiment Variant
- Experiment Cookie

The Google Experiment object contains of an experiment id and an optional alias which can used to alternatively reference the experiment in code.

The Experiment Variant is optional and it is used to give each experiment variant an alias for easier usage in templates/views. If not added, the returned variant will be the index of the variant in the Google Optimize experiment cookie(_gaexp).

The Experiment Cookie is optional and it is only used in DEBUG mode. It aids in overriding or adding an experiment to the browser cookie(_gaexp). Replaces any interaction with the browser session while developing, making it possible to test out all your variants via the Django admin.
