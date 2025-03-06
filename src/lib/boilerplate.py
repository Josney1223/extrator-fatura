import re


def current(tokens: list[str], index: int, offset=0):
    return tokens[index+offset] if index+offset < len(tokens) else None


def find_date(text: str):
    return re.search(r"\b\d{2}/\d{2}(?!/\d{4})\b", text)


def find_monetary(text: str):
    return re.search(r"\b\d+(?:,\d+)+\b", text)


def is_record(text: str, bad_records: str) -> bool:
    return not any(bad_record in text for bad_record in bad_records)
