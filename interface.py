from styles import format_apa, format_bibtex, format_mla

_FORMATTERS = {
    "apa": format_apa,
    "bibtex": format_bibtex,
    "mla": format_mla,
}


def format_ref(ref, style):
    """Format a reference dict in the requested citation style.

    Args:
        ref: dict with keys 'authors' (list of {'last': str, 'first': str}),
             'year', 'title', and optionally 'journal', 'volume', 'number', 'pages'.
        style: one of 'apa', 'bibtex', 'mla' (case-insensitive).

    Returns:
        Formatted citation string.

    Raises:
        ValueError: if style is not supported.
    """
    key = style.lower()
    if key not in _FORMATTERS:
        supported = ", ".join(_FORMATTERS)
        raise ValueError(f"Unknown style '{style}'. Supported: {supported}")
    return _FORMATTERS[key](ref)
