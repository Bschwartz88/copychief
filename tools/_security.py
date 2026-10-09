"""Small shared checks at document output boundaries."""
import re
from urllib.parse import urlsplit


def safe_comment_id(value) -> str:
    """Comment identifiers enter raw HTML/XML attributes; accept only bounded integers."""
    if type(value) not in (int, str):
        raise ValueError("Comment IDs must be nonnegative integers.")
    text = str(value)
    if not re.fullmatch(r"0|[1-9][0-9]{0,9}", text) or int(text) > 2_147_483_647:
        raise ValueError("Comment IDs must be nonnegative 32-bit integers.")
    return text


def safe_url(url: str) -> str:
    """Allow web/email links, never script, file, UNC or credential-bearing URLs."""
    if not isinstance(url, str) or re.search(r"[\s\x00-\x1f\x7f\\]", url):
        raise ValueError("Unsafe hyperlink: whitespace, controls or backslashes.")
    try:
        parsed = urlsplit(url)
        if parsed.scheme.lower() in {"https", "http"} and parsed.hostname and not parsed.username and not parsed.password:
            _ = parsed.port
            return url
        if parsed.scheme.lower() == "mailto" and parsed.path and not parsed.netloc:
            return url
    except ValueError:
        pass
    raise ValueError("Unsafe hyperlink: only HTTP, HTTPS and mailto are supported.")
