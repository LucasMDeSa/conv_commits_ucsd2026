"""citekit — minimal citation formatter for academic references."""


def format_apa(ref):
    """Format a reference dict in APA 7th edition style.

    Args:
        ref: dict with keys 'author_last', 'author_first', 'year', 'title',
             and optionally 'journal'.
    """
    author = f"{ref['author_last']}, {ref['author_first'][0]}."
    citation = f"{author} ({ref['year']}). {ref['title']}."
    if "journal" in ref:
        citation += f" {ref['journal']}."
    return citation


def format_bibtex(ref):
    """Format a reference dict as a BibTeX @article entry.

    Args:
        ref: dict with keys 'author_last', 'author_first', 'year', 'title',
             and optionally 'journal'.
    """
    key = f"{ref['author_last'].lower()}{ref['year']}"
    entry = f"@article{{{key},\n"
    entry += f"  author  = {{{ref['author_last']}, {ref['author_first']}}},\n"
    entry += f"  year    = {{{ref['year']}}},\n"
    entry += f"  title   = {{{ref['title']}}}"
    if "journal" in ref:
        entry += f",\n  journal = {{{ref['journal']}}}"
    entry += "\n}"
    return entry
