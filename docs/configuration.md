# Configuration

The configuration is a list of dicts and each dict consists of three fields, one being mandatory and the other two being optional:

- id(string, required): Experiment id required to identify each experiment in the cookie set by Google.
- alias(string, optional): Alias for the experiment id, useful for clarity when accessing experiment variants by key.
- variant_aliases(dict, optional): Aliases for each variant, consist of key-value variables. The key represents the index for each experiment variant. The value is the alias for the variant. Check your Google Optimize experiment to see which index represents what experiment variant.

## Single experiment

For a single experiment the settings could be the following:

```py
# django-google-optimize
GOOGLE_OPTIMIZE_EXPERIMENTS = [
    {
        "id": "utSuKi3PRbmxeG08en8VNw",
        "alias": "redesign",
        "variant_aliases": {0: "old_design", 1: "new_design"},
    }
]
```

## Multiple experiments

For multiple experiments the settings could be the following:

```py
# django-google-optimize
GOOGLE_OPTIMIZE_EXPERIMENTS = [
    {
        "id": "3x8_BbSCREyqtWm1H1OUrQ",
        "alias": "redesign_page",
        "variant_aliases": {0: "old_design", 1: "new_design"},
    },
    {
        "id": "7IXTpXmLRzKwfU-Eilh_0Q",
        "alias": "redesign_header",
        "variant_aliases": {0: "old_header", 1: "new_header"},
    },
]
```

## Notes

If you do not set the alias you'll have to access the experiment variant by the Google Optimize id for the experiment.

If you do not set the variant alias for a variant the index will be the variant returned.
