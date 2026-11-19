"""!
@file safe_urls.py
@brief Checking of the URLs of the data before a template puts them in a page.
"""

from urllib.parse import quote, urlsplit

from portfolio.constants import (
    FALLBACK_URL,
    IMAGES_DIR_NAME,
    IMAGES_URL_PREFIX,
    SAFE_URL_SCHEMES,
)
from portfolio.domain.validation import is_local_image_path

_LOCAL_IMAGE_PREFIX = f"{IMAGES_DIR_NAME}/"


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
    @brief Give a URL that is safe to put in `href`, before escaping.
    @param url The URL from the data.
    @return The URL without surrounding space, or `#` when it is not safe.
    """
    return url.strip() if is_safe_url(url) else FALLBACK_URL


def image_src(url: str | None) -> str | None:
    """!
    @brief Give the `src` of an image of the data, or None when there is none to show.

    A local path of the images folder (`images/a.png`) becomes the address the
    images route serves (`/images/a.png`); an absolute http or https address is
    kept. Anything else, such as `javascript:`, `data:` or a path with `..`, gives
    None, so the page shows a placeholder.
    @param url The image URL or path from the data; None or empty when there is none.
    @return The address to put in `src`, before escaping, or None.
    """
    if not url:
        return None
    if is_local_image_path(url) and url.startswith(_LOCAL_IMAGE_PREFIX):
        return IMAGES_URL_PREFIX + quote(
            url.removeprefix(_LOCAL_IMAGE_PREFIX), safe="/"
        )
    if is_safe_url(url) and urlsplit(url.strip()).scheme:
        return url.strip()
    return None
