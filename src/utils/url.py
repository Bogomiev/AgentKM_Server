import re

from starlette.requests import Request

url_fix_pattern = r"(?<!:)(\/{2,})"
url_fix_pattern_re = re.compile(url_fix_pattern)


def url_fix(url, *, separator: str = "/"):
    """Исправить множество слэшей в url на один"""
    return url_fix_pattern_re.sub(separator, url)


def _url_fix(url: str, *, sep: str) -> str:
    new_url = url.replace(" ", "") \
        .strip(sep)
    return new_url


def url_concat(*urls: str):
    """Соединить части урлов вместе (только http и https схемы)"""
    if len(urls) == 0:
        raise ValueError("Не переданы параметры")

    separator: str = "/"

    if urls[0].replace(":", "").replace(separator, "") in ("http", "https"):
        raise ValueError("Нельзя передавать отдельно схему как элемент для составления URL")

    result = separator.join([_url_fix(url, sep=separator) for url in urls])
    if not result.startswith("http") and not result.startswith(separator):
        result = separator + result

    return result


ENDPOINT_PATTERN = r"^(?P<versioning>/api/v[\d\.]+)?(?P<endpoint>/(?P<app>[^/\s]*)(/\S+)?)"
ENDPOINT_PATTERN_RE = re.compile(ENDPOINT_PATTERN)


def get_endpoint_by_request(request: Request) -> str:
    """Получить endpoint из HTTP запроса"""
    path = request.url.path
    match = ENDPOINT_PATTERN_RE.match(path)
    if match is None:
        raise ValueError("Не удалось получить endpoint из HTTP запроса")

    app = match.group("app")
    return app
