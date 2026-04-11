"""citekit — minimal citation formatter for academic references."""


def format_apa(ref):
    """Format a reference dict in APA 7th edition style.

    Args:
        ref: dict with keys 'authors' (list of {'last': str, 'first': str}),
             'year', 'title', and optionally 'journal'.
    """
    authors = ref["authors"]
    if len(authors) == 1:
        a = authors[0]
        author_str = f"{a['last']}, {a['first'][0]}."
    elif len(authors) == 2:
        a, b = authors
        author_str = f"{a['last']}, {a['first'][0]}., & {b['last']}, {b['first'][0]}."
    else:
        a = authors[0]
        author_str = f"{a['last']}, {a['first'][0]}., et al."
    citation = f"{author_str} ({ref['year']}). {ref['title']}."
    if "journal" in ref:
        citation += f" {ref['journal']}."
    return citation


def format_mla(ref):
    """Format a reference dict in MLA 9th edition style.

    Args:
        ref: dict with keys 'authors' (list of {'last': str, 'first': str}),
             'year', 'title', and optionally 'journal'.
    """
    authors = ref["authors"]
    if len(authors) == 1:
        author_str = f"{authors[0]['last']}, {authors[0]['first']}"
    elif len(authors) == 2:
        a, b = authors
        author_str = f"{a['last']}, {a['first']}, and {b['first']} {b['last']}"
    else:
        a = authors[0]
        author_str = f"{a['last']}, {a['first']}, et al."
    citation = f'{author_str}. "{ref["title"]}."'
    if "journal" in ref:
        citation += f" {ref['journal']},"
    citation += f" {ref['year']}."
    return citation


def format_bibtex(ref):
    """Format a reference dict as a BibTeX @article entry.

    Args:
        ref: dict with keys 'authors' (list of {'last': str, 'first': str}),
             'year', 'title', and optionally 'journal', 'volume', 'number', 'pages'.
    """
    key = f"{ref['authors'][0]['last'].lower().replace(' ', '')}{ref['year']}"
    author_field = " and ".join(
        f"{a['last']}, {a['first']}" for a in ref["authors"]
    )
    entry = f"@article{{{key},\n"
    entry += f"  author  = {{{author_field}}},\n"
    entry += f"  year    = {{{ref['year']}}},\n"
    entry += f"  title   = {{{ref['title']}}}"
    for field in ("journal", "volume", "number", "pages"):
        if field in ref:
            entry += f",\n  {field:<8}= {{{ref[field]}}}"
    entry += "\n}"
    return entry
