import pypdf
import re
from src.lib.boilerplate import current, is_record


def process_pdf_btg(reader: pypdf.PdfReader) -> list[list[str]]:
    bad_records = []
    register = None
    registers = []

    for page in reader.pages:
        tokens = page.extract_text().split('\n')
        index = 0
        for index in range(len(tokens)):
            actual = current(tokens, index)
            next_token = current(tokens, index+1)
            record = find_register_btg(actual)
            record_date = find_register_date_btg(next_token)
            if record_date is None or record is None:
                continue

            monthStr = record_date.group()[-3:]
            record_month = month_name_to_number(monthStr)

            if is_record(actual, bad_records) and record_month:
                date_str = record_date.group().replace(" "+monthStr, "/"+record_month)
                money_str = find_monetary_btg(record.group()).group()

                description = actual.replace(
                    date_str, "").replace(money_str, "")
                description = description.replace("R$", "").strip()

                register = [date_str]
                register.append(description)
                register.append(money_str)
                registers.append(register)
                register = None
                continue

    return registers


def find_register_btg(text: str):
    return re.search(r"(R|US)\$\s?\d+(?:,\d{2})?\w+(.*)", text)


def find_register_date_btg(text: str):
    return re.search(r"\d{2} \w+", text)


def find_monetary_btg(text: str):
    return re.search(r"\b\d+(?:,\d+)", text)


def month_name_to_number(month: str) -> int:
    meses = {
        'jan': '01',
        'fev': '2',
        'mar': '3',
        'abr': '4',
        'mai': '5',
        'jun': '6',
        'jul': '7',
        'ago': '8',
        'set': '9',
        'out': '10',
        'nov': '11',
        'dez': '12'
    }

    return meses.get(month.lower(), "")
