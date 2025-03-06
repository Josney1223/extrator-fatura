import pypdf
import logging
import sys
from src.extrator_itau import process_pdf_itau
from src.extrator_btg import process_pdf_btg

logging.getLogger().setLevel(logging.DEBUG)


def main():
    bank = sys.argv[1]
    doc = sys.argv[2]

    if doc == "":
        raise Exception("Documento invalido")

    reader = pypdf.PdfReader(doc)

    logging.info(f'Number of pages in "{doc}": ' + str(len(reader.pages)))
    logging.info(f'Bank {bank}')

    if bank == "itau":
        registers = process_pdf_itau(reader)
    elif bank == "btg":
        registers = process_pdf_btg(reader)
    else:
        raise Exception("Erro banco nao cadastrado")

    output_csv(registers)


def output_csv(registers: list[list[str]]):
    headers = ['date', 'description', 'value']
    sep = ';'
    with open('ouput.csv', 'w') as f:
        data = sep.join(headers) + '\n'
        for register in registers:
            data += sep.join(register) + ' \n'
        f.write(data)


if __name__ == "__main__":
    main()
