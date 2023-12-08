from docx import Document
import json

def read_docx(input_path):
    doc = Document(input_path)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text


def get_all_paragraphs(docx_text):
    string = docx_text

    blocks_dick = {
        "Number": "",
        "Period": "",
        "Predmet": "",
        "Mesto": "",
        "IKZ": "",
        "Istochnik": "",
        "Summa": "",
        "Avans": "",
        "Podpisant": ""
    }

    index_number = string.find("№ ")
    endline_num = string.find("\n", index_number)
    blocks_dick['Number'] = string[index_number:endline_num]

    index_period = string.find("заключения Договора до ")+23
    endline_per = string.find(", ", index_period)
    blocks_dick['Period'] = string[index_period:endline_per]

    index_predmet=string.find("в обусловленный срок –")+23
    endline_predmet = string.find(".\n", index_predmet)
    blocks_dick['Predmet'] = string[index_predmet:endline_predmet]

    index_mesto = string.find("г. ")+3
    endline_mesto = string.find("\t", index_mesto)
    blocks_dick['Mesto'] = string[index_mesto:endline_mesto]

    index_ikz = string.find("ИКЗ: ")+5
    endline_ikz = string.find("\n",index_ikz)
    blocks_dick['IKZ'] = string[index_ikz:endline_ikz]

    index_istochnik = string.find("Источник финансирования: ")+25
    endline_istochnik = string.find(".\n", index_istochnik)
    blocks_dick['Istochnik'] = string[index_istochnik:endline_istochnik]

    index_summa = string.find("Цена настоящего договора ")+25
    endline_summa = string.find(". ", index_summa)
    blocks_dick['Summa'] = string[index_summa:endline_summa]

    index_avans = string.find("2.5. ")+5
    endline_avans = string.find("\n", index_avans)
    blocks_dick['Avans'] = string[index_avans:endline_avans]

    # index_podpisant = string.find("")
    # endline_podpisant = string.find("\n")
    # blocks_dick['Podpisant'] = string[index_podpisant:endline_podpisant]

    print(blocks_dick)
    return blocks_dick


if __name__ == "__main__":
    input_docx_path = 'A.docx'

    docx_text = read_docx(input_docx_path)

    with open("blocks.json", "w", encoding='utf-8') as outfile:
        json.dump(get_all_paragraphs(docx_text), outfile, ensure_ascii=False)


    print(docx_text)
