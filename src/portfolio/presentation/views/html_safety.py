"""!
@file html_safety.py
@brief Escaping of text and checking of URLs, for every value put in a page.
"""

import html
from urllib.parse import urlsplit

from portfolio.constants import FALLBACK_URL, SAFE_URL_SCHEMES


def escape(value: str) -> str:
    """!
    @brief Escape a value for use as HTML text or inside a quoted attribute.
    @param value The raw value.
    @return The value with `&`, `<`, `>`, `"` and `'` replaced by entities.
    """
    return html.escape(value, quote=True)


def is_safe_url(url: str) -> bool:
    """!
    @brief Tell whether a URL is an http or https address or a relative path.
    @param url The URL to check.
    @return True when a browser may follow it without running script.
    """
    candidate = url.strip()
    if not candidate or not candidate.isprintable() or "\\" in candidate:
        return False
    try:
        parts = urlsplit(candidate)
    except ValueError:
        return False
    if parts.scheme:
        return parts.scheme.lower() in SAFE_URL_SCHEMES and bool(parts.netloc)
    return not parts.netloc


def safe_url(url: str) -> str:
    """!
    @brief Give a URL that is safe to put in `href` or `src`, before escaping.
    @param url The URL from the data.
    @return The URL without surrounding space, or `#` when it is not safe.
    """
    return url.strip() if is_safe_url(url) else FALLBACK_URL
