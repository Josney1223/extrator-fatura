import pypdf
from src.lib.boilerplate import current, find_monetary, find_date, is_record


def process_pdf_btg(reader: pypdf.PdfReader, doc_name: str):
    # TODO: Nao funciona ainda
    bad_records = []
    register = None
    registers = []

    for page in reader.pages:
        tokens = page.extract_text().split('\n')
        index = 0
        for index in range(len(tokens)):
            actual = current(tokens, index)
            date = find_date(actual)
            money = find_monetary(actual)
            print(actual)

            if date and money and is_record(actual, bad_records):
                date_str = date.group()
                money_str = money.group()

                description = actual.replace(
                    date_str, "").replace(money_str, "").strip()

                register = [date_str]
                register.append(description)
                register.append(money_str)
                registers.append(register)
                register = None
                continue

    return registers
