import pypdf
from src.lib.boilerplate import current, find_date, find_monetary, is_record


def process_pdf_itau(reader: pypdf.PdfReader) -> list[list[str]]:
    # TODO: Diferenciar compras dessa fatura e da próxima
    bad_records: list[str] = ["Pagamento efetuado"]
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
