import re
import datetime

from flask import current_app


def parse_null(value):
    if value is None:
        return ""
    return str(value)


def string(value, limit):
    if len(parse_null(value).strip()) > limit and current_app.config['XML_VALIDATION_ENABLED']:
        raise ImportError(value)
    value = parse_null(value).strip()[:limit]
    return value if len(value) > 1 else ""


def positive_integer(value):
    if not isinstance(value, int):
        try:
            value = int(value)
        except:
            if current_app.config['XML_VALIDATION_ENABLED']:
                raise ImportError(value)
            return -1
    if value < 1:
        if current_app.config['XML_VALIDATION_ENABLED']:
            raise ImportError(value)
        return -1
    return value


def snils(value):
    if value is None:
        return ""
    snils_pattern = re.compile(r"^\d{11}$")
    if snils_pattern.match(value):
        return value
    if current_app.config['XML_VALIDATION_ENABLED']:
        raise ImportError(value)
    return ""


def date(value):
    if value is None:
        return ""
    try:
        return datetime.datetime.strptime(value, "%d.%m.%Y").date()
    except ValueError:
        if current_app.config['XML_VALIDATION_ENABLED']:
            raise ImportError(value)
        return ""
