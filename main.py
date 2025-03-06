import pypdf
import re
import logging
import sys


logging.getLogger().setLevel(logging.DEBUG)


def main():
    doc = sys.argv[1]
    doc_name = doc.split('/')[-1]
    reader = pypdf.PdfReader(doc)

    logging.info(f'Number of pages in "{doc}": ' + str(len(reader.pages)))
    registers = process_pdf(reader, doc_name)
    output_excel(registers)


def process_pdf(reader: pypdf.PdfReader, doc_name: str):
    # TODO: Diferenciar compras dessa fatura e da próxima
    register = None
    registers = []

    for page in reader.pages:
        tokens = page.extract_text().split('\n')
        index = 0
        for index in range(len(tokens)):
            actual = current(tokens, index)
            date = find_date(actual)
            money = find_monetary(actual)

            if date and money and is_record(actual):
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


def current(tokens: list[str], index: int, offset=0):
    return tokens[index+offset] if index+offset < len(tokens) else None


def find_date(text: str):
    return re.search(r"\b\d{2}/\d{2}(?!/\d{4})\b", text)


def find_monetary(text: str):
    return re.search(r"\b\d+(?:,\d+)+\b", text)


def is_record(text: str) -> bool:
    bad_records: list[str] = ["Pagamento efetuado"]
    for i in bad_records:
        if text.find(i) != -1:
            return False
    return True


def output_excel(registers: list[list[str]]):
    sep = ';'
    with open('ouput.csv', 'w') as f:
        data = sep.join(['date', 'description', 'value']) + '\n'
        for register in registers:
            data += sep.join(register) + ' \n'
        f.write(data)


if __name__ == "__main__":
    main()
