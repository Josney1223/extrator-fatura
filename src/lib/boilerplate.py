import re


def current(tokens: list[str], index: int, offset=0):
    # Retorna o token atual dentro de um offset
    return tokens[index+offset] if index+offset < len(tokens) else ""


def find_date(text: str):
    # Retorna se existe uma data no formato DD/MM sem /YYYY
    return re.search(r"\b\d{2}/\d{2}(?!/\d{4})\b", text)


def find_monetary(text: str):
    # Retorna se existe um numero no formato 00,00
    return re.search(r"\b\d+(?:,\d+)+\b", text)


def is_record(text: str, bad_records: str) -> bool:
    # Verifica se o text existe dentro dos bad_records
    return not any(bad_record in text for bad_record in bad_records)
